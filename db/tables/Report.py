from db.tables.Base import Base

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum, Integer, Text, ForeignKey, select
from sqlalchemy.dialects.mysql import MEDIUMTEXT
import enum

import pandas as pd
from sqlalchemy.orm import Session
from db.database import connect

class ReportType(enum.Enum):
    AmbulanceReport = 0
    ReleaseReport = 1

class Report(Base):
    __tablename__ = "Report"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    cispac: Mapped[int] = mapped_column(Integer, ForeignKey('Pacient.id'))  # "CISPAC" as ID

    type: Mapped[ReportType] = mapped_column(Enum(ReportType))
    body: Mapped[str] = mapped_column(MEDIUMTEXT, default="")

    pacient: Mapped[list["Pacient"]] = relationship(back_populates="report_entries", cascade="all")

    def __repr__(self) -> str:
        return f"Report(ID={self.id!r}, PacID={self.cispac!r}, Type={self.type!r}, Body={(self.body[:20] + "...")!r})"
    
    @classmethod
    def insert(cls, reports: list, reportType: ReportType):
        if reports is None or len(reports) == 0:
            raise Exception("reports are empty or None")
        
        con,_ = connect()
        if con is None:
            raise Exception("Database connection failed")
        session = Session(con)

        dbReports = [Report(cispac=u.id, type=reportType, body=u.body) for u in reports]
        cls.insert_missing_ids(list(set([int(u.id) for u in reports])), con)

        # from db.tables.Pacient import Pacient

        # TODO wrong, it filters by pacient id but there can be multiple
        # new_ids = [int(id) for id in df['cispac'].unique()]
        # existing_ids = set(
        #     r[0] for r in session.execute(select(Pacient.id).where(Pacient.id.in_(new_ids)))
        # )
        #         # Filter out the IDs that already exist
        # filtered_rows = df[df['cispac'].isin(set(new_ids) - existing_ids)]
        # Create the objects only for the filtered rows (those that don't already exist)

        try:
            print(f"Inserting {len(dbReports)} data...")
            session.bulk_save_objects(dbReports)
            session.commit()
            print(f"Inserted {len(dbReports)}/{len(dbReports)} rows into Report({reportType}). (unique/all)")
        except Exception as e:
            session.rollback()
            print("Error inserting data:", e)
        finally:
            session.close()




