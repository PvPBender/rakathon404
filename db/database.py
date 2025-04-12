from sqlalchemy import create_engine, Engine, Connection
from dotenv import load_dotenv
from typing import Tuple
import os

load_dotenv()



engine = create_engine(f"mysql+mysqlconnector://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}/{os.getenv("DB_NAME")}", echo=False)

def connect() -> Tuple[Connection, Engine]:
    """Connect to the database."""
    try:
        connection = engine.connect()
        print("Connection successful.")
        return connection, engine
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None
    
def batch_insert(session, data: list, chunk_size: int = 1000, dbName: str = "database"):
    # Insert users in chunks to avoid memory overload
    print(f"Batch inserting into {dbName} {len(data)} records in {chunk_size} chunks.")
    inserted = 0
    for i in range(0, len(data), chunk_size):
        chunk = data[i:i + chunk_size]
        session.add_all(chunk)  # Add all users in the chunk
        session.commit()  # Commit the chunk to the database
        inserted += len(chunk)
        print(f"Inserted {inserted}/{len(data)} records into {dbName}.")
