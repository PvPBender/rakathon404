# LabHem.py
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, Integer, Float, DateTime, ForeignKey, select
from db.tables.Base import Base  # make sure to import your Base class from the same package

import pandas as pd
from sqlalchemy.orm import Session
from db.database import connect

class LabHem(Base):
    __tablename__ = "LabHem"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)  # "ID" as ID
    cispac: Mapped[int] = mapped_column(Integer, ForeignKey('Pacient.id'))  # "CISPAC" as ID

    # CSV columns
    ordnum: Mapped[int] = mapped_column(Integer, nullable=True)        # ORDNUM
    daynum: Mapped[str] = mapped_column(String(16), nullable=True)        # DAYNUM
    orddate: Mapped[datetime] = mapped_column(DateTime, nullable=True) # ORDDATE
    sex: Mapped[str] = mapped_column(Text, nullable=True)            # SEX
    departm: Mapped[str] = mapped_column(Text, nullable=True)        # DEPARTM
    dg1: Mapped[str] = mapped_column(Text, nullable=True)            # DG1
    dg2: Mapped[str] = mapped_column(Text, nullable=True)            # DG2
    dg3: Mapped[str] = mapped_column(Text, nullable=True)            # DG3
    dg4: Mapped[str] = mapped_column(Text, nullable=True)            # DG4
    dg5: Mapped[str] = mapped_column(Text, nullable=True)            # DG5
    dgtxt: Mapped[str] = mapped_column(Text, nullable=True)          # DGTXT
    entrydate: Mapped[datetime] = mapped_column(DateTime, nullable=True)# ENTRYDATE
    height: Mapped[float] = mapped_column(Float, nullable=True)        # HEIGHT
    weight: Mapped[float] = mapped_column(Float, nullable=True)        # WEIGHT
    metd: Mapped[str] = mapped_column(Text, nullable=True)           # METD
    valnum: Mapped[float] = mapped_column(Float, nullable=True)        # VALNUM
    valtxt: Mapped[str] = mapped_column(Text, nullable=True)         # VALTXT
    vallimit: Mapped[str] = mapped_column(Text, nullable=True)       # VALLIMIT
    valcomment: Mapped[str] = mapped_column(Text, nullable=True)     # VALCOMMENT
    valdescr: Mapped[str] = mapped_column(Text, nullable=True)       # VALDESCR
    machine: Mapped[str] = mapped_column(Text, nullable=True)        # MACHINE

    pacient: Mapped["Pacient"] = relationship("Pacient", back_populates="lab_hem_entries", cascade="all")

    def __repr__(self) -> str:
        return (
            f"LabHem("
            f"cispac={self.cispac!r}, ordnum={self.ordnum!r}, daynum={self.daynum!r}, "
            f"orddate={self.orddate!r}, sex={self.sex!r}, departm={self.departm!r}, "
            f"dg1={self.dg1!r}, dg2={self.dg2!r}, dg3={self.dg3!r}, dg4={self.dg4!r}, dg5={self.dg5!r}, "
            f"dgtxt={self.dgtxt!r}, entrydate={self.entrydate!r}, height={self.height!r}, "
            f"weight={self.weight!r}, metd={self.metd!r}, valnum={self.valnum!r}, "
            f"valtxt={self.valtxt!r}, vallimit={self.vallimit!r}, valcomment={self.valcomment!r}, "
            f"valdescr={self.valdescr!r}, machine={self.machine!r}"
            f")"
        )

    
    @classmethod
    def insert(cls, df: pd.DataFrame):
        con,_ = connect()
        if df is None or df.empty:
            raise Exception("DataFrame is empty or None")
        
        if con is None:
            raise Exception("Database connection failed")
        
        
        df.columns = [col.lower() for col in df.columns]
        df['cispac'] = pd.to_numeric(df['cispac'], errors='coerce')
        cls.insert_missing_cispac(df, con)

        session = Session(con)
        from db.tables.Pacient import Pacient


        chunk_size = 1000
        total_inserted = 0
        total_rows = len(df)

        # Process in chunks
        for start in range(0, total_rows, chunk_size):
            # Get the chunk of the DataFrame
            chunk = df.iloc[start:start + chunk_size]

            # Create objects for the filtered rows
            entries = [cls(**row.dropna().to_dict()) for _, row in chunk.iterrows()]

            try:
                session.bulk_save_objects(entries)
                session.commit()

                total_inserted += len(entries)
                print(f"Inserted {total_inserted}/{total_rows} rows into LabHem. ({len(entries)} inserted in this chunk)")
            except Exception as e:
                session.rollback()
                print("Error inserting data:", e)

        # Close the session
        session.close()