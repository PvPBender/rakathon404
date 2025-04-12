import pandas as pd
from datetime import datetime
from sqlalchemy import String, Float, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .Base import Base


# --- Table 1: material_all.csv ---
class HospitalReport(Base):
    __tablename__ = "hospital_report"

    serial: Mapped[float] = mapped_column(primary_key=True)
    cdokl: Mapped[int] = mapped_column(Integer, nullable=True)
    datum: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    typ: Mapped[int] = mapped_column(Integer, nullable=True)
    kod: Mapped[float] = mapped_column(Float, nullable=True)
    zvl: Mapped[int] = mapped_column(Integer, nullable=True)
    lokalizace: Mapped[str] = mapped_column(String, nullable=True)
    oddeleni: Mapped[str] = mapped_column(String, nullable=True)
    mnozstvi: Mapped[float] = mapped_column(Float, nullable=True)
    cenauziv: Mapped[float] = mapped_column(Float, nullable=True)
    cena: Mapped[float] = mapped_column(Float, nullable=True)
    serialcdb: Mapped[float] = mapped_column(Float, nullable=True)
    cispac: Mapped[int] = mapped_column(Integer, nullable=True)
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
    __tablename__ = "annotated_performance"

    serial: Mapped[float] = mapped_column(primary_key=True)
    cdokl: Mapped[int] = mapped_column(Integer, nullable=True)
    datum: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    kod: Mapped[str] = mapped_column(String, nullable=True)
    nazev_vykonu: Mapped[str] = mapped_column(String, nullable=True)
    odbornost: Mapped[float] = mapped_column(Float, nullable=True)
    lokalizace: Mapped[str] = mapped_column(String, nullable=True)
    oddeleni: Mapped[float] = mapped_column(Float, nullable=True)
    mnozstvi: Mapped[int] = mapped_column(Integer, nullable=True)
    body: Mapped[float] = mapped_column(Float, nullable=True)
    cenamat: Mapped[float] = mapped_column(Float, nullable=True)
    cenauziv: Mapped[float] = mapped_column(Float, nullable=True)
    cena: Mapped[float] = mapped_column(Float, nullable=True)
    serialcdb: Mapped[float] = mapped_column(Float, nullable=True)
    cispac: Mapped[int] = mapped_column(Integer, nullable=True)
    cispac_z_uctu: Mapped[float] = mapped_column(Float, nullable=True)
    rok: Mapped[int] = mapped_column(Integer, nullable=True)

    def __repr__(self) -> str:
        return (
            f"AnnotatedPerformance(serial={self.serial}, datum={self.datum}, "
            f"kod={self.kod}, nazev_vykonu={self.nazev_vykonu}, cispac={self.cispac})"
        )
