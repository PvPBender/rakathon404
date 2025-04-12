import json
from dataclasses import asdict
from model.patientTemplate import PacientTemplate

def savePatient(file_name: str, patient: PacientTemplate):
    patient_dict = asdict(patient)
    # Save to JSON file
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(patient_dict, f, ensure_ascii=False, indent=4)

def loadPatient(file_name: str) -> PacientTemplate:
    with open(file_name, "r", encoding="utf-8") as f:
        patient_dict = json.load(f)
    return PacientTemplate(**patient_dict)
