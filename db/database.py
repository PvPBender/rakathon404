from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

# Import all tables here before Base
from db.tables.Patient import Pacient
from db.tables.LabBio import BioLab
from db.tables.LabHem import LabHem
from db.tables.Patolog import Patolog

from db.tables.Base import Base


engine = create_engine(f"mysql+mysqlconnector://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}/{os.getenv("DB_NAME")}", echo=True)

def connect():
    """Connect to the database."""
    try:
        connection = engine.connect()
        print("Connection successful.")
        Base.metadata.create_all(engine)  # Create tables if they don't exist
        return connection
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None