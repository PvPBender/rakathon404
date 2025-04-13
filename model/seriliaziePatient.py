import json
from dataclasses import asdict
from datetime import datetime
from model.patientTemplate import PacientTemplate


def savePatient(file_name: str, patient: PacientTemplate):
    # Convert to dict and ensure empty lists are included
    patient_dict = asdict(patient)

    # Ensure M_B2 and M_C are included even if empty
    patient_dict.setdefault('M_B_2', [])
    patient_dict.setdefault('M_C', [])

    # Save to JSON file with datetime handling
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(
            patient_dict,
            f,
            ensure_ascii=False,
            indent=4,
            default=lambda o: o.isoformat() if isinstance(o, datetime) else str(o)
        )
