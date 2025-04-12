import pandas as pd
from model.patientTemplate import PacientTemplate

def build_patient(df: pd.DataFrame, cispac_value: str) -> PacientTemplate:
    patient = PacientTemplate()
    patient.m_1.m_1_1.m_1_1_4 = [cispac_value]
    return patient

