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
from sqlalchemy import func, text, distinct, exists, or_
from db.tables import Patolog, Report, Rentgen, HospitalReport, AnnotatedPerformance


def main():
    cispac_value = 2354488
    patient = build_patient(cispac_value)

    try:
        connection, engine = connect()
        with Session(bind=engine) as session:
            
            # Query to find patient with most records
            patients_with_records = (
                select(Pacient.id)
                .where(
                    or_(
                        exists().where(Patolog.cispac == Pacient.id),
                        exists().where(Report.cispac == Pacient.id),
                        exists().where(Rentgen.cispac == Pacient.id),
                        exists().where(AnnotatedPerformance.cispac == Pacient.id)
                    )
                )
                .where(
                    ~exists().where(HospitalReport.cispac == Pacient.id)
                )
            )

            patient_with_most_records = (
                select(
                    Pacient.id,
                    (
                        func.count(distinct(Patolog.id))
                        + func.count(distinct(Report.id))
                        + func.count(distinct(Rentgen.id))
                        + func.count(distinct(AnnotatedPerformance.id))
                    ).label("total_records"),
                )
                .outerjoin(Patolog, Pacient.id == Patolog.cispac)
                .outerjoin(Report, Pacient.id == Report.cispac)
                .outerjoin(Rentgen, Pacient.id == Rentgen.cispac)
                .outerjoin(
                    AnnotatedPerformance, Pacient.id == AnnotatedPerformance.cispac
                )
                .where(Pacient.id.in_(patients_with_records))
                .group_by(Pacient.id)
                .order_by(text("total_records DESC"))
                .limit(1)
            )

            # cispac_value = session.execute(patient_with_most_records).unique().scalar_one_or_none()
            cispac_value = 0
            logging.info(f"Pacient ID: {cispac_value}")
            print(f"Patient with the most records: {cispac_value}")
            # print(f"Pacient data: {pacient_data.pat_entries}")
            # print(f"Pacient data: {pacient_data}")

            stmt = (
                select(Pacient)
                .where(Pacient.id == cispac_value)
                .options(
                    joinedload(Pacient.pat_entries),
                    # joinedload(Pacient.lab_bio_entries),
                    # joinedload(Pacient.lab_hem_entries),
                    joinedload(Pacient.report_entries),
                    joinedload(Pacient.rentgen_entries),
                    joinedload(Pacient.hospital_report_entries)
                )
            )

            pacient_data = session.execute(stmt).unique().scalar_one_or_none()

            if pacient_data:
                logging.info(f"Patolog entries: {pacient_data.pat_entries}")
                print(f"Patolog entries: {len(pacient_data.pat_entries)}")
                # logging.info(f"BioLab entries: {pacient_data.lab_bio_entries}")
                # logging.info(f"HemLab entries: {pacient_data.lab_hem_entries}")
                logging.info(f"Report entries: {pacient_data.report_entries}")
                print(f"Report entries: {len(pacient_data.report_entries)}")
                logging.info(f"Rentgen entries: {pacient_data.rentgen_entries}")
                print(f"Rentgen entries: {len(pacient_data.rentgen_entries)}")
                logging.info(f"Hospital report entries: {pacient_data.hospital_report_entries}")
                print(f"Hospital report entries: {len(pacient_data.hospital_report_entries)}")

            patient = loadDataToPatient(patient, pacient_data)

        savePatient(f"patient_{cispac_value}.json", patient)

    except SQLAlchemyError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
