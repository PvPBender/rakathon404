import pandas as pd
from model.patientTemplate import PacientTemplate, IdentifikatorPacienta
from model.patientTemplateModuleC import PacientTemplateModuleC as MC

from db.tables.Pacient import Pacient
from loader.handlePat import handlePat
from loader.handleBio import handleBio
from loader.handleHem import handleHem
from loader.handleReport import handleReport
from loader.handleRentgen import handleRentgen

from model.patientTemplateModuleA import MA1
from model.patientTemplateModuleB2 import PacientTemplateModuleB2 as MB2
from model.patientTemplateModuleB2 import MB21, MB22, MB23, MB24, MB25
from model.patientTemplateModuleC import MC2, MC3, MC4, MC5, MC6, MC7, MC8, MC9, MC10, MC11, MC12
import logging
from datetime import date
from model.patientTemplateModuleC import MakroskopickeRezidum
from model.patientTemplateModuleC import AnoNeUdaj


def build_patient(cispac_value: str) -> PacientTemplate:
    patient = PacientTemplate()
    # patient.M_1.M_1_1.M_1_1_4.append(IdentifikatorPacienta(typ="cispac", identifikator=str(cispac_value)))
    patient.M_1.M_1_1.M_1_1_4 = cispac_value
    patient.M_B_2 = []
    MB2_1 = MB2()
    MB2_1.M_B_2_1 = MB21()  # Initialize MB21 instance
    # MB2_1.M_B_2_1.M_B_2_1_1 = "Provedeno"
    patient.M_B_2.append(MB2_1)

    MB2_2 = MB2()
    MB2_2.M_B_2_2 = MB22()  # Initialize MB22 instance
    patient.M_B_2.append(MB2_2)

    MB2_3 = MB2()
    MB2_3.M_B_2_3 = MB23()  # Initialize MB23 instance
    patient.M_B_2.append(MB2_3)

    MB2_4 = MB2()
    MB2_4.M_B_2_4 = MB24()  # Initialize MB24 instance
    patient.M_B_2.append(MB2_4)

    MB2_5 = MB2()
    MB2_5.M_B_2_5 = MB25()  # Initialize MB25 instance
    patient.M_B_2.append(MB2_5)

    patient.M_C = []

    MC_1 = MC()
    
    MC_3 = MC3()
    MC_1.M_C_3 = MC_3
    
    # MC_4 = MC4(
    #     M_C_4_1=date.today(),  # Required date field
    #     M_C_4_6=AnoNeUdaj.NE,  # Required enum field
    #     M_C_4_7=AnoNeUdaj.NE   # Required enum field
    # )
    # MC_1.M_C_4 = MC_4

    MC_5 = MC5()
    MC_1.M_C_5 = MC_5

    MC_6 = MC6()
    MC_1.M_C_6 = MC_6
    
    patient.M_C.append(MC_1)

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
