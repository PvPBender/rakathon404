import pandas as pd
from typing import Dict, List, Optional
import os
from dotenv import load_dotenv
from sqlalchemy.exc import SQLAlchemyError
from loader.buildPatient import build_patient
from loader.handleBio import handleBio
from loader.handleHem import handleHem
from loader.handlePat import handlePatolog
from loader.handlePatientData import handlePatientData
from model.seriliaziePatient import savePatient
from db.database import connect
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
import logging
from loader.handleReport import handleReport
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from sqlalchemy.future import select
from db.tables.Patient import Pacient



def load_filtered(connection, table_name, column_name, cispac_value):
    query = text(f"SELECT * FROM {table_name} WHERE {column_name} = :cispac")
    result = connection.execute(query, {"cispac": cispac_value})
    return [dict(row) for row in result]


def main():
    
    cispac_value = int("YOUR_CISPAC_VALUE")

    try:
        connection = connect()

        # Assuming `conn` is your Connection instance
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
            
            pacient = session.execute(stmt).scalar_one_or_none()

            if pacient:
                logging.info(f"Patolog entries: {pacient.pat_entries}")
                logging.info(f"BioLab entries: {pacient.lab_bio_entries}")
                logging.info(f"LabHem entries: {pacient.lab_hem_entries}")
                logging.info(f"Report entries: {pacient.report_entries}")


            patient = build_patient(cispac_value)

            for pat_entry in pacient.pat_entries:
                handlePatolog(pat_entry, patient)

            for biolab_entry in pacient.lab_bio_entries:
                handleBio(biolab_entry, patient)

            for labhem_entry in pacient.lab_hem_entries:
                handleHem(labhem_entry, patient)    
            
            for report_entry in pacient.report_entries:
                handleReport(report_entry, patient)
        savePatient(f"patient_{cispac_value}.json", patient)
          
    except SQLAlchemyError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
