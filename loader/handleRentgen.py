from typing import List
from dataclasses import field
from model.patientTemplate import PacientTemplate
from db.tables.Rentgen import Rentgen
from model.patientTemplateModuleA import MA13, MA2, PacientTemplateModuleA


def extract_komorbidity_from_text(text: str, patient: PacientTemplate):
    """Extrahuje známé komorbidity z textu a ukládá je do PacientTemplate.M_A.M_A_1.M_A_1_3"""

    if not text:
        return

    if not patient.M_A.M_A_1.M_A_1_3:
        patient.M_A.M_A_1.M_A_1_3 = MA13()

    ma13 = patient.M_A.M_A_1.M_A_1_3

    komorbidity_map = {
        "CHOPN": ("M_A_1_3_3", "CHOPN"),
        "astma": ("M_A_1_3_3", "astma"),
        "diabetes": ("M_A_1_3_2", "diabetes mellitus"),
        "cukrovka": ("M_A_1_3_2", "diabetes mellitus"),
        "hypertenze": ("M_A_1_3_1", "hypertenze"),
        "vysoký tlak": ("M_A_1_3_1", "hypertenze"),
        "infarkt": ("M_A_1_3_1", "infarkt myokardu"),
        "cmp": ("M_A_1_3_1", "cévní mozková příhoda"),
        "mozková příhoda": ("M_A_1_3_1", "cévní mozková příhoda"),
        "ten": ("M_A_1_3_1", "TEN"),
        "selhání ledvin": ("M_A_1_3_5", "chronické renální selhání"),
        "hepatitida": ("M_A_1_3_10", "hepatitida B"),
        "covid": ("M_A_1_3_10", "COVID-19"),
        "hiv": ("M_A_1_3_10", "HIV"),
    }

    text_lower = text.lower()

    for keyword, (field, value) in komorbidity_map.items():
        if keyword in text_lower:
            current_value = getattr(ma13, field, "")
            if value.lower() not in current_value.lower():
                setattr(ma13, field, value)


def handleRentgen(rentgen_entries: List[Rentgen], patient: PacientTemplate) -> PacientTemplate:
    """Zpracuje rentgenová data a doplní je do PacientTemplate.M_A"""

    if not rentgen_entries:
        return patient

    entry = rentgen_entries[0]

    # --- Antropometrie (M_A_2) ---
    if not patient.M_A.M_A_2:
        patient.M_A.M_A_2.append(MA2())

    antropo = patient.M_A.M_A_2[0]

    try:
        if entry.vyska and entry.vyska.isdigit():
            antropo.M_A_2_2 = float(entry.vyska)

        if entry.hmotnost and entry.hmotnost.isdigit():
            antropo.M_A_2_3 = float(entry.hmotnost)

        if antropo.M_A_2_2 and antropo.M_A_2_3:
            height_m = antropo.M_A_2_2 / 100
            bmi = round(antropo.M_A_2_3 / (height_m ** 2), 2)
            antropo.M_A_2_4 = bmi
    except Exception as e:
        print(f"[WARN] BMI výpočet selhal: {e}")

    if entry.vysldat:
        antropo.M_A_2_1 = entry.vysldat.strftime('%Y-%m-%d')

    # --- Komorbidity z textu ---
    full_text = " ".join(filter(None, [entry.popis, entry.txt1, entry.txt2, entry.dgkoment]))
    extract_komorbidity_from_text(full_text, patient)

    return patient
