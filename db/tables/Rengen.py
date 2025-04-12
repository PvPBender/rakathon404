
from db.tables.Base import Base
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Text, Integer, DateTime, ForeignKey

"""
ODDEL,CISPAC,POHLAVI,DG1,DG2,DG3,DG4,DG5,DGKOMENT,DATUM,PROODBORNOST,NALUZKUPRIM,TXT1,ODDELZPRACOVAL,POPIS,TYPSUBJEKTU,KODSUBJEKTU,PRAC,CISRTGPRAC,PRISTROJ,TXT2,POZNVYS,CISZAD1,VYSKA,HMOTNOST,VYSETRMETD,VYSLDAT,POPIS_POZNAMKA,CISPAC.1,RTG_DATA_CONTENT 
"""

class Rengen(Base):
    __tablename__ = "Rengen"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    oddel: Mapped[str] = mapped_column(Text, nullable=True)  # "ODDEL"
    cispac: Mapped[int] = mapped_column(Integer, ForeignKey('Pacient.id'))  # "CISPAC"
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

    pacient: Mapped[list["Pacient"]] = relationship(back_populates="rengen_entries", cascade="all")

    def __repr__(self) -> str:
        return (
            f"Rengen("
            f"id={self.id!r}, "
            f"cispac={self.cispac!r}, "
            f"datum={self.datum!r}, "
            f"..."
            f")"
        )





