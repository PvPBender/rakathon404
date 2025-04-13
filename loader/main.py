import pandas as pd
from sqlalchemy.exc import SQLAlchemyError
from loader.buildPatient import build_patient, loadDataToPatient
from model.seriliaziePatient import savePatient
from db.database import connect
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from sqlalchemy.future import select
from db.tables.Pacient import Pacient
import logging
from datetime import datetime
from parsers.utils import pathTo

def main():
    cispac_value = 98332
    patient = build_patient(cispac_value)

    try:
        connection, engine = connect()
        with Session(bind=engine) as session:
            stmt = (
                select(Pacient)
                .where(Pacient.id == cispac_value)
                .options(
                    joinedload(Pacient.pat_entries),
                    # joinedload(Pacient.lab_bio_entries),
                    # joinedload(Pacient.lab_hem_entries),
                    joinedload(Pacient.report_entries),
                    joinedload(Pacient.rentgen_entries)
                )
            )

            pacient_data = session.execute(stmt).unique().scalar_one_or_none()

            print(f"Pacient data: {pacient_data.pat_entries}")

            if pacient_data:
                logging.info(f"Patolog entries: {pacient_data.pat_entries}")
                # logging.info(f"BioLab entries: {pacient_data.lab_bio_entries}")
                # logging.info(f"HemLab entries: {pacient_data.lab_hem_entries}")
                logging.info(f"Report entries: {pacient_data.report_entries}")
                logging.info(f"Rentgen entries: {pacient_data.rentgen_entries}")

            patient = loadDataToPatient(patient, pacient_data)
            
        savePatient(pathTo("loader", "reports", f"patient_{cispac_value}.json"), patient)

    except SQLAlchemyError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
