import pandas as pd
from datetime import datetime
from sqlalchemy import Text, Float, Integer, DateTime, ForeignKey, select
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .Base import Base
from sqlalchemy import ForeignKey

import pandas as pd
from sqlalchemy.orm import Session
from db.database import connect, batch_insert

# --- Table 1: material_all.csv ---
class HospitalReport(Base):
    __tablename__ = "HospitalReport"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    cispac: Mapped[int] = mapped_column(Integer, ForeignKey('Pacient.id'))  # "CISPAC"
    
    serial: Mapped[float] = mapped_column(primary_key=True)
    cdokl: Mapped[int] = mapped_column(Integer, nullable=True)
    datum: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    typ: Mapped[int] = mapped_column(Integer, nullable=True)
    kod: Mapped[float] = mapped_column(Float, nullable=True)
    zvl: Mapped[int] = mapped_column(Integer, nullable=True)
    lokalizace: Mapped[str] = mapped_column(Text, nullable=True)
    oddeleni: Mapped[str] = mapped_column(Text, nullable=True)
    mnozstvi: Mapped[float] = mapped_column(Float, nullable=True)
    cenauziv: Mapped[float] = mapped_column(Float, nullable=True)
    cena: Mapped[float] = mapped_column(Float, nullable=True)
    serialcdb: Mapped[float] = mapped_column(Float, nullable=True)
    cispac_z_uctu: Mapped[float] = mapped_column(Float, nullable=True)
    rok: Mapped[int] = mapped_column(Integer, nullable=True)
    
    pacient: Mapped[list["Pacient"]] = relationship(back_populates="hospital_report_entries", cascade="all")
    
    def __repr__(self) -> str:
        return (
            f"HospitalReport(serial={self.serial}, datum={self.datum}, "
            f"kod={self.kod}, cispac={self.cispac}, cena={self.cena})"
        )


# --- Table 2: vykony_annotated.csv ---
class AnnotatedPerformance(Base):
    __tablename__ = "AnnotatedPerformance"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    cispac: Mapped[int] = mapped_column(Integer, ForeignKey('Pacient.id'))  # "CISPAC"
    cispac_z_uctu: Mapped[float] = mapped_column(Float, nullable=True)

    serial: Mapped[float] = mapped_column(primary_key=True)
    cdokl: Mapped[int] = mapped_column(Integer, nullable=True)
    datum: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    kod: Mapped[str] = mapped_column(Text, nullable=True)
    nazev_vykonu: Mapped[str] = mapped_column(Text, nullable=True)
    odbornost: Mapped[float] = mapped_column(Float, nullable=True)
    lokalizace: Mapped[str] = mapped_column(Text, nullable=True)
    oddeleni: Mapped[float] = mapped_column(Float, nullable=True)
    mnozstvi: Mapped[int] = mapped_column(Integer, nullable=True)
    body: Mapped[float] = mapped_column(Float, nullable=True)
    cenamat: Mapped[float] = mapped_column(Float, nullable=True)
    cenauziv: Mapped[float] = mapped_column(Float, nullable=True)
    cena: Mapped[float] = mapped_column(Float, nullable=True)
    serialcdb: Mapped[float] = mapped_column(Float, nullable=True)
    rok: Mapped[int] = mapped_column(Integer, nullable=True)

    pacient: Mapped[list["Pacient"]] = relationship(back_populates="annotated_perf_entries", cascade="all")

    def __repr__(self) -> str:
        return (
            f"AnnotatedPerformance(serial={self.serial}, datum={self.datum}, "
            f"kod={self.kod}, nazev_vykonu={self.nazev_vykonu}, cispac={self.cispac})"
        )

    @classmethod
    def insert(cls, df: pd.DataFrame):
        if df is None or df.empty:
            raise Exception("DataFrame is empty or None")
        
        con,_ = connect()
        if con is None:
            raise Exception("Database connection failed")
        
        
        df.columns = [col.lower() for col in df.columns]
        df['cispac'] = pd.to_numeric(df['cispac'], errors='coerce')
        cls.insert_missing_cispac(df, con)

        session = Session(con)
        from db.tables.Pacient import Pacient

        # TODO wrong, it filters by pacient id but there can be multiple
        # new_ids = [int(id) for id in df['cispac'].unique()]
        # existing_ids = set(
        #     r[0] for r in session.execute(select(Pacient.id).where(Pacient.id.in_(new_ids)))
        # )
        #         # Filter out the IDs that already exist
        # filtered_rows = df[df['cispac'].isin(set(new_ids) - existing_ids)]
        # # Create the objects only for the filtered rows (those that don't already exist)
        entries = [cls(**row.dropna().to_dict()) for _, row in df.iterrows()]


        batch_insert(session, entries, 100, "AnnotatedPerf")
        session.close()

