import pandas as pd
from model.patientTemplate import PacientTemplate, IdentifikatorPacienta

from db.tables.Patient import Pacient
from loader.handlePat import handlePat
from loader.handleBio import handleBio
from loader.handleHem import handleHem
from loader.handleReport import handleReport
from loader.handleRengen import handleRengen

from model.patientTemplateModuleA import MA1


def build_patient(cispac_value: str) -> PacientTemplate:
    patient = PacientTemplate()
    patient.M_1.M_1_1.M_1_1_4.append(IdentifikatorPacienta(typ="cispac", identifikator=str(cispac_value)))
    return patient


def loadDataToPatient(patient: PacientTemplate, pacient_data: Pacient):
    for pat_entry in pacient_data.pat_entries:
        handlePat(pat_entry, patient)

    for biolab_entry in pacient_data.lab_bio_entries:
        handleBio(biolab_entry, patient)

    for labhem_entry in pacient_data.lab_hem_entries:
        handleHem(labhem_entry, patient)

    for report_entry in pacient_data.report_entries:
        handleReport(report_entry, patient)

    for rengen_entry in pacient_data.rengen_entries:
        handleRengen(rengen_entry, patient)

    return patient
