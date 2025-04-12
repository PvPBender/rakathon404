# Patolog.py
from db.tables.Base import Base

from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Text, Integer, DateTime, ForeignKey, select
from sqlalchemy.dialects.mysql import MEDIUMTEXT

import pandas as pd
from sqlalchemy.orm import Session

from db.database import connect

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
    dodatek1: Mapped[str] = mapped_column(MEDIUMTEXT, nullable=True)    # "DODATEK1"
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
        new_ids = [int(id) for id in df['cispac'].unique()]
        existing_ids = set(
            r[0] for r in session.execute(select(Pacient.id).where(Pacient.id.in_(new_ids)))
        )
                # Filter out the IDs that already exist
        filtered_rows = df[df['cispac'].isin(set(new_ids) - existing_ids)]
        # Create the objects only for the filtered rows (those that don't already exist)
        entries = [cls(**row.dropna().to_dict()) for _, row in filtered_rows.iterrows()]



        try:
            session.bulk_save_objects(entries)
            session.commit()
            print(f"Inserted {len(entries)}/{len(new_ids)} rows into Patolog. (unique/all)")
        except Exception as e:
            session.rollback()
            print("Error inserting data:", e)
        finally:
            session.close()

        # for index, row in df.iterrows():
        #     pRow = cls(**row.dropna().to_dict())
        #     try:
        #         # Insert row into the database
        #         session.add(pRow)  # Or your actual insert statement
        #         session.commit()
        #     except Exception as e:
        #         session.rollback()
        #         print(f"Error inserting row {index}: {e}")
        #         print("Row", pRow)
