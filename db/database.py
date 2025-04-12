from sqlalchemy import create_engine, Engine, Connection
from dotenv import load_dotenv
from typing import Tuple
import os

load_dotenv()



engine = create_engine(f"mysql+mysqlconnector://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}/{os.getenv("DB_NAME")}", echo=True)

def connect() -> Tuple[Connection, Engine]:
    """Connect to the database."""
    try:
        connection = engine.connect()
        print("Connection successful.")
        return connection, engine
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None