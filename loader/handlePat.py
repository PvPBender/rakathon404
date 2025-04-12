import logging
import json
import openai


from db.tables import Patolog
from model.patientTemplate import PacientTemplate
from model.patientTemplateModuleB1 import MB1
from model.patientTemplateModuleB1 import (
    Lateralita, BiologickeChovani, TNM_CT, TNM_CN, TNM_CM
)


def detect_lateralita(*lokality: str) -> str:
    lokality_text = " ".join(filter(None, lokality)).lower()

    vpravo = "prav" in lokality_text
    vlevo = "lev" in lokality_text

    if vpravo and vlevo:
        return Lateralita.OBOUSTRANNE
    elif vpravo:
        return Lateralita.VPRAVO
    elif vlevo:
        return Lateralita.VLEVO
    elif "střed" in lokality_text or "centr" in lokality_text:
        return Lateralita.ODPADA
    else:
        return Lateralita.NEZNAMO



def analyze_text_with_gpt(text: str) -> dict:
    print("TEXT PRO GPT:")
    print(text + "\n")
    system_msg = """
    Tvým úkolem je z patologického nebo klinického textu vytěžit klíčové onkologické parametry dle Modulu B1 ÚZIS.
    Odpověz výhradně ve formátu JSON.
    
    Pole:
    - klasifikace_nadoru
    - klinicka_T, klinicka_N, klinicka_M
    - patologicka_T, patologicka_N, patologicka_M
    - biologicke_chovani
    - diagnosticka_skupina
    - relaps_datum
    - relaps_typ
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            temperature=0,
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": text}
            ]
        )
        return json.loads(response["choices"][0]["message"]["content"])
    except Exception as e:
        logging.warning(f"OpenAI GPT extraction failed: {e}")
        return {}


def handlePat(pat_entry: Patolog, patient: PacientTemplate):
    logging.info(f"Handling PAT: {pat_entry}")

    # ---- přímé údaje ----
    # M1
    patient.M_1.M_1_1.M_1_1_1 = pat_entry.cislosub
    patient.M_1.M_1_1.M_1_1_2 = pat_entry.rok
    patient.M_1.M_1_1.M_1_1_3 = pat_entry.datum
    patient.M_1.M_1_1.M_1_1_4 = pat_entry.datumvysl
    patient.M_1.M_1_1.M_1_1_6 = pat_entry.pohlavi

    # MB1 – klasifikace a typ vzorku
    patient.M_B1.M_B_1.M_B_1_2_1 = pat_entry.dgpat or pat_entry.dg or pat_entry.dg1
    patient.M_B1.M_B_1.M_B_1_2_8 = pat_entry.typvzorku

    # MB1 – lateralita z lokalit
    lat_value = detect_lateralita(pat_entry.lokal1, pat_entry.lokal2, pat_entry.lokal3)
    patient.M_B1.M_B_1.M_B_1_2_5 = lat_value

    # ---- GPT – volný text ----
    fulltext = "\n".join(filter(None, [pat_entry.klindg, pat_entry.text]))
    if fulltext.strip():
        gpt_output = analyze_text_with_gpt(fulltext)
        logging.info(f"GPT návrh: {json.dumps(gpt_output, indent=2, ensure_ascii=False)}")

        # Ruční mapování výsledků
        if "klasifikace_nadoru" in gpt_output:
            patient.M_B.M_B_1.M_B_1_2_1 = gpt_output["klasifikace_nadoru"]

        if "klinicka_T" in gpt_output:
            val = gpt_output["klinicka_T"].replace("T", "").replace("p", "")
            patient.M_B.M_B_1.M_B_1_3_1_1 = TNM_CT(value=val)

        if "klinicka_N" in gpt_output:
            val = gpt_output["klinicka_N"].replace("N", "").replace("p", "")
            patient.M_B.M_B_1.M_B_1_3_1_3 = TNM_CN(value=val)

        if "klinicka_M" in gpt_output:
            val = gpt_output["klinicka_M"].replace("M", "").replace("p", "")
            patient.M_B.M_B_1.M_B_1_3_1_4 = TNM_CM(value=val)

        if "patologicka_T" in gpt_output:
            val = gpt_output["patologicka_T"].replace("T", "").replace("p", "")
            patient.M_B.M_B_1.M_B_1_3_2_4 = TNM_CT(value=val)

        if "patologicka_N" in gpt_output:
            val = gpt_output["patologicka_N"].replace("N", "").replace("p", "")
            patient.M_B.M_B_1.M_B_1_3_2_6 = TNM_CN(value=val)

        if "patologicka_M" in gpt_output:
            val = gpt_output["patologicka_M"].replace("M", "").replace("p", "")
            patient.M_B.M_B_1.M_B_1_3_2_12 = TNM_CM(value=val)

        if "biologicke_chovani" in gpt_output:
            patient.M_B.M_B_1.M_B_1_2_11 = BiologickeChovani(value=gpt_output["biologicke_chovani"])

        if "diagnosticka_skupina" in gpt_output:
            patient.M_B.M_B_1.M_B_1_4_1 = gpt_output["diagnosticka_skupina"]

        if "relaps_datum" in gpt_output:
            patient.M_B.M_B_1.M_B_3_2_2 = gpt_output["relaps_datum"]

        if "relaps_typ" in gpt_output:
            patient.M_B.M_B_1.M_B_3_2_2_1 = gpt_output["relaps_typ"]

    return patient
