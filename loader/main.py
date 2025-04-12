import pandas as pd
from sqlalchemy.exc import SQLAlchemyError
from loader.buildPatient import build_patient, loadDataToPatient
from model.seriliaziePatient import savePatient
from db.database import connect
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from sqlalchemy.future import select
from db.tables.Patient import Pacient
import logging
from datetime import datetime

def main():
    cispac_value = int("YOUR_CISPAC_VALUE")

    try:
        connection = connect()
        with Session(bind=connection) as session:
            stmt = (
                select(Pacient)
                .where(Pacient.id == cispac_value)
                .options(
                    joinedload(Pacient.pat_entries),
                    joinedload(Pacient.lab_bio_entries),
                    joinedload(Pacient.lab_hem_entries),
                    joinedload(Pacient.report_entries),
                )
            )

            pacient_data = session.execute(stmt).scalar_one_or_none()

            if pacient_data:
                logging.info(f"Patolog entries: {pacient_data.pat_entries}")
                logging.info(f"BioLab entries: {pacient_data.lab_bio_entries}")
                logging.info(f"HemLab entries: {pacient_data.lab_hem_entries}")
                logging.info(f"Report entries: {pacient_data.report_entries}")
                logging.info(f"Rentgen entries: {pacient_data.rentgen_entries}")

            patient = build_patient(cispac_value)
            patient = loadDataToPatient(patient, pacient_data)
            
        savePatient(f"patient_{cispac_value}.json", patient)

    except SQLAlchemyError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
