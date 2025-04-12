
from db.tables.Base import Base
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Text, Integer, DateTime, ForeignKey, select


import pandas as pd
from sqlalchemy.orm import Session
from db.database import connect, batch_insert


class Rentgen(Base):
    __tablename__ = "Rentgen"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    cispac: Mapped[int] = mapped_column(Integer, ForeignKey('Pacient.id'))  # "CISPAC"

    oddel: Mapped[str] = mapped_column(Text, nullable=True)  # "ODDEL"
    pohlavi: Mapped[str] = mapped_column(Text, nullable=True)  # "POHLAVI"
    dg1: Mapped[str] = mapped_column(Text, nullable=True)  # "DG1"
    dg2: Mapped[str] = mapped_column(Text, nullable=True)  # "DG2"
    dg3: Mapped[str] = mapped_column(Text, nullable=True)  # "DG3"
    dg4: Mapped[str] = mapped_column(Text, nullable=True)  # "DG4"
    dg5: Mapped[str] = mapped_column(Text, nullable=True)  # "DG5"
    dgkoment: Mapped[str] = mapped_column(Text, nullable=True)  # "DGKOMENT"
    datum: Mapped[datetime] = mapped_column(DateTime, nullable=True)  # "DATUM"
    proodbornost: Mapped[str] = mapped_column(Text, nullable=True)  # "PROODBORNOST"
    naluzkuprim: Mapped[str] = mapped_column(Text, nullable=True)  # "NALUZKUPRIM"
    txt1: Mapped[str] = mapped_column(Text, nullable=True)  # "TXT1"
    oddelzpracoval: Mapped[str] = mapped_column(Text, nullable=True)  # "ODDELZPRACOVAL"
    popis: Mapped[str] = mapped_column(Text, nullable=True)  # "POPIS"
    typsubjektu: Mapped[str] = mapped_column(Text, nullable=True)  # "TYPSUBJEKTU"
    kodsubjektu: Mapped[str] = mapped_column(Text, nullable=True)  # "KODSUBJEKTU"
    prac: Mapped[str] = mapped_column(Text, nullable=True)  # "PRAC"
    cisrtgprac: Mapped[str] = mapped_column(Text, nullable=True)  # "CISRTGPRAC"
    pristroj: Mapped[str] = mapped_column(Text, nullable=True)  # "PRISTROJ"
    txt2: Mapped[str] = mapped_column(Text, nullable=True)  # "TXT2"
    poznvys: Mapped[str] = mapped_column(Text, nullable=True)  # "POZNVYS"
    ciszad1: Mapped[str] = mapped_column(Text, nullable=True)  # "CISZAD1"
    vyska: Mapped[str] = mapped_column(Text, nullable=True)  # "VYSKA"
    hmotnost: Mapped[str] = mapped_column(Text, nullable=True)  # "HMOTNOST"
    vysetrmetd: Mapped[str] = mapped_column(Text, nullable=True)  # "VYSETRMETD"
    vysldat: Mapped[datetime] = mapped_column(DateTime, nullable=True)  # "VYSLDAT"
    popis_poznamka: Mapped[str] = mapped_column(Text, nullable=True)  # "POPIS_POZNAMKA"
    cispac_1: Mapped[int] = mapped_column(Integer, nullable=True)  # "CISPAC.1"
    rtg_data_content: Mapped[str] = mapped_column(Text, nullable=True)  # "RTG_DATA_CONTENT"

    pacient: Mapped[list["Pacient"]] = relationship(back_populates="rentgen_entries", cascade="all")

    def __repr__(self) -> str:
        return (
            f"Rentgen("
            f"id={self.id!r}, "
            f"cispac={self.cispac!r}, "
            f"datum={self.datum!r}, "
            f"..."
            f")"
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


        batch_insert(session, entries, 100, "Rentgen")
        session.close()



