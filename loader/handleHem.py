import pandas as pd
from model.patientTemplate import PacientTemplate
from db.tables.LabHem import LabHem
import math

def handleHem(hemlab_entry: list[LabHem], patient: PacientTemplate):
    patient.m_1.m_1_1.m_1_1_6 = hemlab_entry.sex

    last_measurement_date = patient.m_a.m_a_2.m_a_2_1

    if last_measurement_date is None or hemlab_entry.entrydate > last_measurement_date:
        patient.m_a.m_a_2.m_a_2_1 = hemlab_entry.entrydate
        patient.m_a.m_a_2.m_a_2_2 = hemlab_entry.height
        patient.m_a.m_a_2.m_a_2_3 = hemlab_entry.weight
        bmi = hemlab_entry.weight / (hemlab_entry.height ** 2)
        patient.m_a.m_a_2.m_a_2_4 = bmi
        # BSA = √(weight (kg) × height (cm) / 3600).
        bsa = math.sqrt(hemlab_entry.weight * hemlab_entry.height / 3600)
        patient.m_a.m_a_2.m_a_2_5 = bsa
        
    return patient