import pandas as pd
from model.patientTemplate import PacientTemplate
import logging

def handlePat(df: pd.DataFrame, patient: PacientTemplate):
    logging.info(f"Handling PAT: {df}")
    return patient