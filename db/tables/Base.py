from sqlite3 import IntegrityError
from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy import Connection
import pandas as pd


class Base(DeclarativeBase):

    @classmethod
    def insert_missing_cispac(cls, df: pd.DataFrame, con: Connection, column_name: str = 'cispac') -> list[int]:
        """
        Insert missing values from a specified column into the Pacient table.
        This function is case-insensitive and will use the provided column name.e
        returns a list of missing IDs that were inserted.
        """
        df.columns = [col.lower() for col in df.columns]
        if column_name not in df.columns:
            raise ValueError(f"The column '{column_name}' does not exist in the DataFrame.")

        # Ensure the column names in the dataframe are lowercase for consistency
        pacient_ids_from_df = [int(id_str) for id_str in df[column_name].unique()]
        return cls.insert_missing_ids(pacient_ids_from_df, con)

    @classmethod
    def insert_missing_ids(cls, ids: list[int], con: Connection) -> list[int]:
        session = Session(con)

        from db.tables.Pacient import Pacient
        existing_pacient_ids = set(id[0] for id in session.query(Pacient.id).all())
        missing_pacient_ids = [pid for pid in ids if pid not in existing_pacient_ids]
        print(f"Found {len(missing_pacient_ids)} missing IDs to insert.")

        pacient_objects = [Pacient(id=value, year=None, gender=None) for value in missing_pacient_ids]
        try:
            session.add_all(pacient_objects)
            session.commit()
            session.close()
            print("Finished saving missing IDs")
            return ids
        except IntegrityError:
            session.rollback()
            print("IntegrityError: Some IDs may already exist in the Pacient table.")
            session.close()