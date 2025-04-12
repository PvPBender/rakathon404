# BioLab.py
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Float, DateTime
from db.tables.Base import Base  # import your Base class

class BioLab(Base):
    __tablename__ = "LabBio"

    # Primary key
    cispac: Mapped[int] = mapped_column(Integer, primary_key=True)
    
    # CSV columns
    ordnum: Mapped[int] = mapped_column(Integer, nullable=True)        # ORDNUM
    daynum: Mapped[int] = mapped_column(Integer, nullable=True)        # DAYNUM
    orddate: Mapped[datetime] = mapped_column(DateTime, nullable=True) # ORDDATE
    sex: Mapped[str] = mapped_column(String, nullable=True)            # SEX
    departm: Mapped[str] = mapped_column(String, nullable=True)        # DEPARTM
    dg1: Mapped[str] = mapped_column(String, nullable=True)            # DG1
    dg2: Mapped[str] = mapped_column(String, nullable=True)            # DG2
    dg3: Mapped[str] = mapped_column(String, nullable=True)            # DG3
    dg4: Mapped[str] = mapped_column(String, nullable=True)            # DG4
    dg5: Mapped[str] = mapped_column(String, nullable=True)            # DG5
    dgtxt: Mapped[str] = mapped_column(String, nullable=True)          # DGTXT
    entrydate: Mapped[datetime] = mapped_column(DateTime, nullable=True)# ENTRYDATE
    height: Mapped[float] = mapped_column(Float, nullable=True)        # HEIGHT
    weight: Mapped[float] = mapped_column(Float, nullable=True)        # WEIGHT
    metd: Mapped[str] = mapped_column(String, nullable=True)           # METD
    valnum: Mapped[float] = mapped_column(Float, nullable=True)        # VALNUM
    valtxt: Mapped[str] = mapped_column(String, nullable=True)         # VALTXT
    vallimit: Mapped[str] = mapped_column(String, nullable=True)       # VALLIMIT
    valcomment: Mapped[str] = mapped_column(String, nullable=True)     # VALCOMMENT
    valdescr: Mapped[str] = mapped_column(String, nullable=True)       # VALDESCR
    machine: Mapped[str] = mapped_column(String, nullable=True)        # MACHINE

    def __repr__(self) -> str:
        return (
            f"BioLab("
            f"cispac={self.cispac!r}, ordnum={self.ordnum!r}, daynum={self.daynum!r}, "
            f"orddate={self.orddate!r}, sex={self.sex!r}, departm={self.departm!r}, "
            f"dg1={self.dg1!r}, dg2={self.dg2!r}, dg3={self.dg3!r}, dg4={self.dg4!r}, dg5={self.dg5!r}, "
            f"dgtxt={self.dgtxt!r}, entrydate={self.entrydate!r}, height={self.height!r}, "
            f"weight={self.weight!r}, metd={self.metd!r}, valnum={self.valnum!r}, "
            f"valtxt={self.valtxt!r}, vallimit={self.vallimit!r}, valcomment={self.valcomment!r}, "
            f"valdescr={self.valdescr!r}, machine={self.machine!r}"
            f")"
        )
