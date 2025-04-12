import pandas as pd

from db.tables import Patolog
from model.patientTemplate import PacientTemplate, M_1_1
import logging


def handlePat(pat_entry: list[Patolog], patient: PacientTemplate):
    logging.info(f"Handling PAT: {pat_entry}")
    print("------POHLAVI: " + pat_entry.pohlavi)
    print("------ROK: " + str(pat_entry.rok))

    patient.M_1.M_1_1.M_1_1_6 = pat_entry.pohlavi

    return patient