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
    Odpověz výhradně ve formátu JSON. ...
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

        content = response.choices[0].message.content

        if not content or not content.strip():
            logging.warning("GPT response was empty or whitespace only.")
            return {}

        content = content.strip()

        # Odstraň vše před prvním `{`, pokud GPT omylem vygeneroval prefix
        if not content.startswith("{"):
            idx = content.find("{")
            if idx != -1:
                content = content[idx:]

        logging.debug(f"GPT response content:\n{content}")

        return json.loads(content)

    except json.JSONDecodeError as jde:
        logging.error(f"JSON decoding failed: {jde}")
        logging.debug(f"Raw content that caused error: {repr(content)}")
        return {}

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


    def assign_if_str(target, attr_name, value):
        if isinstance(value, str):
            setattr(target, attr_name, value)


    def assign_if_list(target, attr_name, value):
        if isinstance(value, list):
            setattr(target, attr_name, value)

        # ---- GPT – volný text ----


    fulltext = "\n".join(filter(None, [pat_entry.klindg, pat_entry.text]))
    if fulltext.strip():
        gpt_output = analyze_text_with_gpt(fulltext)
        logging.info(
            f"GPT návrh: {json.dumps(gpt_output, indent=2, ensure_ascii=False)}")

        if not isinstance(gpt_output, dict):
            logging.warning("GPT output není slovník.")
            return patient

        assign_if_str(patient.M_B1.M_B_1, "M_B_1_2_1",
                      gpt_output.get("klasifikace_nadoru"))

        if isinstance(gpt_output.get("klinicka_T"), str):
            patient.M_B1.M_B_1.M_B_1_3_1_1 = TNM_CT(
                value=clean_tnm(gpt_output["klinicka_T"], "T"))
        if isinstance(gpt_output.get("klinicka_N"), str):
            patient.M_B1.M_B_1.M_B_1_3_1_3 = TNM_CN(
                value=clean_tnm(gpt_output["klinicka_N"], "N"))
        if isinstance(gpt_output.get("klinicka_M"), str):
            patient.M_B1.M_B_1.M_B_1_3_1_4 = TNM_CM(
                value=clean_tnm(gpt_output["klinicka_M"], "M"))

        if isinstance(gpt_output.get("patologicka_T"), str):
            patient.M_B1.M_B_1.M_B_1_3_2_4 = TNM_CT(
                value=clean_tnm(gpt_output["patologicka_T"], "T"))
        if isinstance(gpt_output.get("patologicka_N"), str):
            patient.M_B1.M_B_1.M_B_1_3_2_6 = TNM_CN(
                value=clean_tnm(gpt_output["patologicka_N"], "N"))
        if isinstance(gpt_output.get("patologicka_M"), str):
            patient.M_B1.M_B_1.M_B_1_3_2_12 = TNM_CM(
                value=clean_tnm(gpt_output["patologicka_M"], "M"))

        val = gpt_output.get("biologicke_chovani")
        if val in BiologickeChovani._value2member_map_:
            patient.M_B1.M_B_1.M_B_1_2_11 = BiologickeChovani(val)
        elif val is not None:
            logging.warning(f"Neplatné biologické chování: {val}")

        assign_if_str(patient.M_B1.M_B_1, "M_B_1_4_1",
                      gpt_output.get("diagnosticka_skupina"))
        assign_if_str(patient.M_B1.M_B_1, "M_B_3_2_2",
                      gpt_output.get("relaps_datum"))
        assign_if_str(patient.M_B1.M_B_1, "M_B_3_2_2_1",
                      gpt_output.get("relaps_typ"))
        assign_if_str(patient.M_B1.M_B_1, "M_B_1_2_6",
                      gpt_output.get("morfologie_slovne"))
        assign_if_str(patient.M_B1.M_B_1, "M_B_1_2_7",
                      gpt_output.get("typ_morfologie"))
        assign_if_str(patient.M_B1.M_B_1, "M_B_1_2_12", gpt_output.get("grading"))
        assign_if_str(patient.M_B1.M_B_1, "M_B_1_3_3", gpt_output.get("stadium"))
        assign_if_list(patient.M_B1.M_B_1, "M_B_1_3_4",
                       gpt_output.get("metastazy_lokalizace"))
        assign_if_str(patient.M_B1.M_B_1, "M_B_1_3_5",
                      gpt_output.get("lymfaticka_invaze"))
        assign_if_str(patient.M_B1.M_B_1, "M_B_1_3_6",
                      gpt_output.get("zilni_invaze"))
        assign_if_str(patient.M_B1.M_B_1, "M_B_1_3_8",
                      gpt_output.get("rezidualni_nador_R"))

        return patient
