from db.tables.Base import Base

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum, Text
import enum

class Gender(enum.Enum):
    male = 0
    female = 1
    other = 2


class Pacient(Base):
    __tablename__ = "Pacient"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=False)
    year: Mapped[int] = mapped_column(Text, nullable=True)  # "ROK"
    gender: Mapped[Gender] = mapped_column(Enum(Gender), nullable=True)  # "POHLAVI"

    pat_entries: Mapped[list["Patolog"]] = relationship(back_populates="pacient", cascade="all, delete-orphan")
    lab_bio_entries: Mapped[list["BioLab"]] = relationship(back_populates="pacient", cascade="all, delete-orphan")
    lab_hem_entries: Mapped[list["LabHem"]] = relationship(back_populates="pacient", cascade="all, delete-orphan")
    report_entries: Mapped[list["Report"]] = relationship(back_populates="pacient", cascade="all, delete-orphan")   
    rentgen_entries: Mapped[list["Rentgen"]] = relationship(back_populates="pacient", cascade="all, delete-orphan")
    hospital_report_entries: Mapped[list["HospitalReport"]] = relationship(back_populates="pacient", cascade="all, delete-orphan")


    def __repr__(self) -> str:
        return f"Pacient(id={self.id!r}, year={self.year!r}, sex={self.gender!r})"
