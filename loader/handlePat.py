import pandas as pd
from model.patientTemplate import PacientTemplate
import logging

def handlePat(pat_entry, patient: PacientTemplate):
    logging.info(f"Handling PAT: {pat_entry}")

    return patient