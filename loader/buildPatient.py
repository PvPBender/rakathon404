import pandas as pd
from model.patientTemplate import PacientTemplate, IdentifikatorPacienta
from model.patientTemplateModuleC import PacientTemplateModuleC

from db.tables.Pacient import Pacient
from loader.handlePat import handlePat
from loader.handleBio import handleBio
from loader.handleHem import handleHem
from loader.handleReport import handleReport
from loader.handleRentgen import handleRentgen

from model.patientTemplateModuleA import MA1

import logging


def build_patient(cispac_value: str) -> PacientTemplate:
    patient = PacientTemplate()
    # patient.M_1.M_1_1.M_1_1_4.append(IdentifikatorPacienta(typ="cispac", identifikator=str(cispac_value)))
    patient.M_1.M_1_1.M_1_1_4 = cispac_value
    return patient


def loadDataToPatient(patient: PacientTemplate, pacient_data: Pacient):
    if not pacient_data:
        logging.error(f"Pacient data not found for {patient.M_1.M_1_1.M_1_1_4}")
        return patient
    
    for pat_entry in pacient_data.pat_entries:
        print(pat_entry)
        print(pat_entry.text)
        handlePat(pat_entry, patient)

    # for biolab_entry in pacient_data.lab_bio_entries:
    #     handleBio(biolab_entry, patient)

    # for hemlab_entry in pacient_data.lab_hem_entries:
    #     handleHem(hemlab_entry, patient)

    for report_entry in pacient_data.report_entries:
        handleReport(report_entry, patient)

    for rentgen_entry in pacient_data.rentgen_entries:
        handleRentgen(rentgen_entry, patient)

    return patient
