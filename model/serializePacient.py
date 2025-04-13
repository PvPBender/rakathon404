import json
import os
from dataclasses import asdict
from model.patientTemplate import PacientTemplate
from parsers.utils import pathTo

OUTPUT_DIR = pathTo("loader", "reports")

def savePacient(file_name: str, patient: PacientTemplate):
    # Convert to dict and ensure empty lists are included
    patient_dict = asdict(patient)

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    
    # Ensure M_B2 and M_C are included even if empty
    if 'M_B2' not in patient_dict:
        patient_dict['M_B2'] = []
        
    if 'M_C' not in patient_dict:
        patient_dict['M_C'] = []
    
    # Save to JSON file
    with open(OUTPUT_DIR / file_name, "w", encoding="utf-8") as f:
        json.dump(patient_dict, f, ensure_ascii=False, indent=4)

def loadPatient(file_name: str) -> PacientTemplate:
    with open(OUTPUT_DIR / file_name, "r", encoding="utf-8") as f:
        patient_dict = json.load(f)
    return PacientTemplate(**patient_dict)
