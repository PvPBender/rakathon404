import pandas as pd
from model.patientTemplate import PacientTemplate

from db.tables.Patient import Pacient
from loader.handlePat import handlePatolog
from loader.handleBio import handleBio
from loader.handleHem import handleHem
from loader.handleReport import handleReport

def build_patient(cispac_value: str) -> PacientTemplate:
    patient = PacientTemplate()
    patient.m_1.m_1_1.m_1_1_4 = [cispac_value]
    return patient

def loadDataToPatient(patient: PacientTemplate, pacient_data: Pacient):
    for pat_entry in pacient_data.pat_entries:
        handlePatolog(pat_entry, patient)

    for biolab_entry in pacient_data.lab_bio_entries:
        handleBio(biolab_entry, patient)

    for labhem_entry in pacient_data.lab_hem_entries:
        handleHem(labhem_entry, patient)

    for report_entry in pacient_data.report_entries:
        handleReport(report_entry, patient)
    
    return patient
