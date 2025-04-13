import pandas as pd
from model.patientTemplate import PacientTemplate
from db.tables.HospitalReport import HospitalReport


def handlePatientData(hospital_reports: list[HospitalReport], patient: PacientTemplate) -> PacientTemplate:
    if not hospital_reports:
        return patient

    # Zkusíme použít první záznam
    report = hospital_reports[0]

    # --- Identifikace pacienta ---
    if report.cispac:
        patient.M_1.M_1_1.M_1_1_4 = report.cispac

    if report.rok:
        patient.M_1.M_1_1.M_1_1_3 = str(report.rok)

    # Mapování typ -> pohlaví (pokud existuje konvence, např. 1=muž, 2=žena)
    if report.typ:
        gender_map = {1: "M", 2: "F"}  # M = muž, F = žena
        patient.M_1.M_1_1.M_1_1_6 = gender_map.get(report.typ, "U")  # U = unknown

    # --- Oddělení (např. jako jazyk) ---
    if report.oddeleni:
        patient.M_1.M_1_1.M_1_1_7 = [report.oddeleni]

    return patient
