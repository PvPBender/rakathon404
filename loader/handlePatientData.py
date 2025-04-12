import pandas as pd
from model.patientTemplate import PacientTemplate
from db.tables.HospitalReport import HospitalReport

def handlePatientData(hospital_report: list[HospitalReport], patient: PacientTemplate):
    return patient