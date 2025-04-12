import pandas as pd
from model.patientTemplate import PacientTemplate
from db.tables.Patient import BioLab
import math

"""
DAYNUM	ORDDATE	CISPACC	SEX	DEPARTM	DG1	DG2	DG3	DG4	DG5	DG TEXT	DAUM VSTUPU	HEIGHT	WEIGHT	METD	VALNUM	VALTXT	VALLIMIT	VALCOMMENT	VALDESCR	MACHINE
DEN OBJEDNÁVKY	DATUM OBJEDNÁVKY	ČÍSLO PACIENTA	POHLAVÍ	ODDĚLENÍ	DIAGNÓZA	DIAGNÓZA	DIAGNÓZA	DIAGNÓZA	DIAGNÓZA	DIAGNÓZA TEXTEM	DATUM VSTUPU	VÝŠKA	VÁHA	METODA						PŘÍSTROJ
"""

"""
M.A.2.1	Datum měření		datum	Povinné		
M.A.2.2	Výška		číslo [cm]	Povinné		1..1
M.A.2.3	Hmotnost		číslo [kg]	Povinné		1..1
M.A.2.4	BMI		číslo	Podmíněně povinné	automatický výpočet	1..1
M.A.2.5	BSA		číslo	Podmíněně povinné	automatický výpočet	1..1
"""

def handleBio(biolab_entry: list[BioLab], patient: PacientTemplate):
    patient.m_1.m_1_1.m_1_1_6 = biolab_entry.sex

    last_measurement_date = patient.m_a.m_a_2.m_a_2_1

    if last_measurement_date is None or biolab_entry.entrydate > last_measurement_date:
        patient.m_a.m_a_2.m_a_2_1 = biolab_entry.entrydate
        patient.m_a.m_a_2.m_a_2_2 = biolab_entry.height
        patient.m_a.m_a_2.m_a_2_3 = biolab_entry.weight
        bmi = biolab_entry.weight / (biolab_entry.height ** 2)
        patient.m_a.m_a_2.m_a_2_4 = bmi
        # BSA = √(weight (kg) × height (cm) / 3600).
        bsa = math.sqrt(biolab_entry.weight * biolab_entry.height / 3600)
        patient.m_a.m_a_2.m_a_2_5 = bsa

    return patient