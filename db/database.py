from sqlalchemy import create_engine

# Import all tables here before Base
from .tables.Patient import Pacient


from .tables.Base import Base

engine = create_engine("mysql+mysqlconnector://root:@localhost/onkominer", echo=True)

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