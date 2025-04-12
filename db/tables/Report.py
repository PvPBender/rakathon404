from db.tables.Base import Base

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum, Integer, Text, ForeignKey
import enum


class ReportType(enum.Enum):
    AmbulanceReport = 0
    ReleaseReport = 1

class Report(Base):
    __tablename__ = "Report"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    cispac: Mapped[int] = mapped_column(Integer, ForeignKey('Pacient.id'))  # "CISPAC" as ID

    type: Mapped[ReportType] = mapped_column(Enum(ReportType))
    body: Mapped[str] = mapped_column(Text)

    pacient: Mapped[list["Pacient"]] = relationship(back_populates="report_entries", cascade="all")

    def __repr__(self) -> str:
        return f"Report(ID={self.id!r}, PacID={self.cispac:r}, Type={self.type!r}, Body={(self.body[:20] + "...")!r})"
