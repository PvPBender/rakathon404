import json
import logging
import os
from enum import Enum
from typing import Optional

from dotenv import load_dotenv
from openai import OpenAI

from db.tables import Patolog
from model.patientTemplate import PacientTemplate
from model.patientTemplateModuleB2 import MB21, MB23, MB24, MB26
from model.patientTemplateModuleB1 import (
    Lateralita, BiologickeChovani, TNM_CT, TNM_CN, TNM_CM
)

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class BiologickeChovani(str, Enum):
    BENIGNI = "0"
    NEJISTE_NEZNAME = "1"
    IN_SITU = "2"
    MALIGNI_PRIMARNI = "3"
    MALIGNI_SEKUNDARNI = "6"


def detect_biologicke_chovani(morf_kod: str) -> str:
    if not morf_kod or "/" not in morf_kod:
        return ""
    suffix = morf_kod.split("/")[-1].strip()
    if suffix in {"0", "1", "2", "3", "6"}:
        return suffix
    return ""


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

    Rozšířená pole:
    - morfologie_slovne
    - typ_morfologie (např. biopsie, cytologie, pitva, jiný)
    - grading (např. G1, G2, G3)
    - stadium (např. I, II, III, IV)
    - metastazy_lokalizace (seznam míst: např. [\"játra\", \"plíce\"])
    - lymfaticka_invaze (např. L0, L1, LX)
    - zilni_invaze (např. V0, V1, V2, VX)
    - rezidualni_nador_R (např. R0, R1, R2, RX)

    Dbej na přesnost kódování dle pravidel TNM a ÚZIS. Pokud údej nelze ze spisu určit, napiš `null`.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            temperature=0,
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": text}
            ]
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        logging.warning(f"OpenAI GPT extraction failed: {e}")
        return {}


MB2_MAPPING = {
    "C71": "MB21",
    "C50": "MB23",
    "C18": "MB26", "C19": "MB26", "C20": "MB26",
    "C61": "MB27",
    "C34": "MB24",
    "C25": "MB30",
}


def map_dg_to_mb2_class(dg_kod: str) -> Optional[str]:
    if not dg_kod:
        return None
    dg_kod = dg_kod.upper().strip()
    for prefix, mb2_class in MB2_MAPPING.items():
        if dg_kod.startswith(prefix):
            return mb2_class
    return None

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
    lat_value = detect_lateralita(pat_entry.lokal1, pat_entry.lokal2,
                                  pat_entry.lokal3)
    patient.M_B1.M_B_1.M_B_1_2_5 = lat_value

    # MB2


    dg_kod = pat_entry.dg or pat_entry.dgpat
    mb2_class_name = map_dg_to_mb2_class(dg_kod)

    # Vytvoř správnou instanci a přiřaď do patient.M_B2
    if mb2_class_name:
        # Dynamicky získej třídu podle názvu (např. MB21)
        mb2_class = globals().get(mb2_class_name)
        if mb2_class:
            # Inicializuj instanci a ulož ji
            setattr(patient.M_B2, mb2_class_name, mb2_class())

            # Ukázka zápisu hodnoty do pole např. exprese ATRX (MB21)
            if mb2_class_name == "MB21":
                if "ATRX pozitivní" in (pat_entry.text or "").lower():
                    getattr(patient.M_B2, "MB21").M_B_2_1_2_4 = "pozitivní"



    def clean_tnm(value: str, typ: str) -> str:
        """
        Odstraní prefixy jako 'T', 'N', 'M', 'p' z TNM klasifikace.
        typ = 'T' nebo 'N' nebo 'M'
        """
        if isinstance(value, str):
            return value.replace(typ, "").replace("p", "").strip()
        return ""

    # ---- GPT – volný text ----
    fulltext = "\n".join(filter(None, [pat_entry.klindg, pat_entry.text]))
    if fulltext.strip():
        gpt_output = analyze_text_with_gpt(fulltext)
        logging.info(
            f"GPT návrh: {json.dumps(gpt_output, indent=2, ensure_ascii=False)}")


        if isinstance(gpt_output.get("klasifikace_nadoru"), str):
            patient.M_B1.M_B_1.M_B_1_2_1 = gpt_output["klasifikace_nadoru"]

        if isinstance(gpt_output.get("klinicka_T"), str):
            val = clean_tnm(gpt_output["klinicka_T"], "T")
            patient.M_B1.M_B_1.M_B_1_3_1_1 = TNM_CT(value=val)

        if isinstance(gpt_output.get("klinicka_N"), str):
            val = clean_tnm(gpt_output["klinicka_N"], "N")
            patient.M_B1.M_B_1.M_B_1_3_1_3 = TNM_CN(value=val)

        if isinstance(gpt_output.get("klinicka_M"), str):
            val = clean_tnm(gpt_output["klinicka_M"], "M")
            patient.M_B1.M_B_1.M_B_1_3_1_4 = TNM_CM(value=val)

        if isinstance(gpt_output.get("patologicka_T"), str):
            val = clean_tnm(gpt_output["patologicka_T"], "T")
            patient.M_B1.M_B_1.M_B_1_3_2_4 = TNM_CT(value=val)

        if isinstance(gpt_output.get("patologicka_N"), str):
            val = clean_tnm(gpt_output["patologicka_N"], "N")
            patient.M_B1.M_B_1.M_B_1_3_2_6 = TNM_CN(value=val)

        if isinstance(gpt_output.get("patologicka_M"), str):
            val = clean_tnm(gpt_output["patologicka_M"], "M")
            patient.M_B1.M_B_1.M_B_1_3_2_12 = TNM_CM(value=val)

        val = gpt_output.get("biologicke_chovani")
        if val in BiologickeChovani._value2member_map_:
            patient.M_B1.M_B_1.M_B_1_2_11 = BiologickeChovani(val)
        else:
            logging.warning(f"Neplatné biologické chování: {val}")

        if isinstance(gpt_output.get("diagnosticka_skupina"), str):
            patient.M_B1.M_B_1.M_B_1_4_1 = gpt_output["diagnosticka_skupina"]

        if isinstance(gpt_output.get("relaps_datum"), str):
            patient.M_B1.M_B_1.M_B_3_2_2 = gpt_output["relaps_datum"]

        if isinstance(gpt_output.get("relaps_typ"), str):
            patient.M_B1.M_B_1.M_B_3_2_2_1 = gpt_output["relaps_typ"]

        if isinstance(gpt_output.get("morfologie_slovne"), str):
            patient.M_B1.M_B_1.M_B_1_2_6 = gpt_output["morfologie_slovne"]

        if isinstance(gpt_output.get("typ_morfologie"), str):
            patient.M_B1.M_B_1.M_B_1_2_7 = gpt_output["typ_morfologie"]

        if isinstance(gpt_output.get("grading"), str):
            patient.M_B1.M_B_1.M_B_1_2_12 = gpt_output["grading"]

        if isinstance(gpt_output.get("stadium"), str):
            patient.M_B1.M_B_1.M_B_1_3_3 = gpt_output["stadium"]

        if isinstance(gpt_output.get("metastazy_lokalizace"), list):
            patient.M_B1.M_B_1.M_B_1_3_4 = gpt_output["metastazy_lokalizace"]

        if isinstance(gpt_output.get("lymfaticka_invaze"), str):
            patient.M_B1.M_B_1.M_B_1_3_5 = gpt_output["lymfaticka_invaze"]

        if isinstance(gpt_output.get("zilni_invaze"), str):
            patient.M_B1.M_B_1.M_B_1_3_6 = gpt_output["zilni_invaze"]

        if isinstance(gpt_output.get("rezidualni_nador_R"), str):
            patient.M_B1.M_B_1.M_B_1_3_8 = gpt_output["rezidualni_nador_R"]

    return patient
