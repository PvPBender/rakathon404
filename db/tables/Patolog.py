# Patolog.py
from db.tables.Base import Base

from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Text, Integer, DateTime, ForeignKey

class Patolog(Base):
    __tablename__ = "Patolog"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)  # "ID" as ID
    cispac: Mapped[int] = mapped_column(Integer, ForeignKey('Pacient.id'))  # "CISPAC" as ID

    subsystem: Mapped[str] = mapped_column(Text, nullable=True)   # "SUBSYSTEM"
    rok: Mapped[int] = mapped_column(Integer, nullable=True)        # "ROK"
    cislosub: Mapped[int] = mapped_column(Integer, nullable=True)   # "CISLOSUB"
    pohlavi: Mapped[str] = mapped_column(Text, nullable=True)     # "POHLAVI"
    datum: Mapped[datetime] = mapped_column(DateTime, nullable=True)# "DATUM"
    datumvysl: Mapped[datetime] = mapped_column(DateTime, nullable=True) # "DATUMVYSL"
    oddel: Mapped[str] = mapped_column(Text, nullable=True)       # "ODDEL"
    dg: Mapped[str] = mapped_column(Text, nullable=True)          # "DG"
    dg1: Mapped[str] = mapped_column(Text, nullable=True)         # "DG1"
    lokal1: Mapped[str] = mapped_column(Text, nullable=True)      # "LOKAL1"
    lokal2: Mapped[str] = mapped_column(Text, nullable=True)      # "LOKAL2"
    lokal3: Mapped[str] = mapped_column(Text, nullable=True)      # "LOKAL3"
    dgpat: Mapped[str] = mapped_column(Text, nullable=True)       # "DGPAT"
    typvzorku: Mapped[str] = mapped_column(Text, nullable=True)   # "TYPVZORKU"
    idzad: Mapped[str] = mapped_column(Text, nullable=True)       # "IDZAD"
    dodatek: Mapped[str] = mapped_column(Text, nullable=True)     # "DODATEK"
    dodatek1: Mapped[str] = mapped_column(Text, nullable=True)    # "DODATEK1"
    priloha: Mapped[str] = mapped_column(Text, nullable=True)     # "PRILOHA"
    priloha1: Mapped[str] = mapped_column(Text, nullable=True)    # "PRILOHA1"
    klindg: Mapped[str] = mapped_column(Text, nullable=True)      # "KLINDG"
    text: Mapped[str] = mapped_column(Text, nullable=True)        # "TEXT"

    pacient: Mapped[list["Pacient"]] = relationship(back_populates="pat_entries", cascade="all")

    def __repr__(self) -> str:
        return (
            f"Patolog("
            f"cispac={self.cispac!r}, "
            f"subsystem={self.subsystem!r}, "
            f"rok={self.rok!r}, "
            f"pohlavi={self.pohlavi!r}, "
            f"datum={self.datum!r}, "
            f"..."
            f")"
        )
