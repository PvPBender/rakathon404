# BioLab.py
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Text, String, Integer, Float, DateTime, ForeignKey
from db.tables.Base import Base  # import your Base class

import pandas as pd
from sqlalchemy.orm import Session
from db.database import connect

class BioLab(Base):
    __tablename__ = "BioLab"

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
    dg3: Mapped[str] = mapped_column(Text, nullable=True)            # DG3 not in use
    dg4: Mapped[str] = mapped_column(Text, nullable=True)            # DG4 not in use
    dg5: Mapped[str] = mapped_column(Text, nullable=True)            # DG5 not in use
    dgtxt: Mapped[str] = mapped_column(Text, nullable=True)          # DGTXT not in use
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

    #pacient: Mapped["Pacient"] = relationship(back_populates="lab_bio_entries", cascade="all")

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
            # # Filter unique cispac IDs to check existing records
            # new_ids = [int(id) for id in chunk['cispac'].unique()]
            # existing_ids = set(
            #     r[0] for r in session.execute(select(Pacient.id).where(Pacient.id.in_(new_ids)))
            # )

            # # Filter rows that do not already exist in the database
            # filtered_chunk = chunk[chunk['cispac'].isin(set(new_ids) - existing_ids)]

            # Create objects for the filtered rows
            entries = [cls(**row.dropna().to_dict()) for _, row in chunk.iterrows()]

            try:
                session.bulk_save_objects(entries)
                session.commit()

                total_inserted += len(entries)
                print(f"Inserted {total_inserted}/{total_rows} rows into HemLab. ({len(entries)} inserted in this chunk)")
            except Exception as e:
                session.rollback()
                print("Error inserting data:", e)

        # Close the session
        session.close()


        # TODO wrong, it filters by pacient id but there can be multiple
        # new_ids = [int(id) for id in df['cispac'].unique()]
        # existing_ids = set(
        #     r[0] for r in session.execute(select(Pacient.id).where(Pacient.id.in_(new_ids)))
        # )
        #         # Filter out the IDs that already exist
        # filtered_rows = df[df['cispac'].isin(set(new_ids) - existing_ids)]
        # Create the objects only for the filtered rows (those that don't already exist)
        # entries = [cls(**row.dropna().to_dict()) for _, row in df.iterrows()]

