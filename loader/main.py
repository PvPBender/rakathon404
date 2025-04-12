import psycopg2
from psycopg2 import sql
import pandas as pd
from typing import Dict, List, Optional
import os
from dotenv import load_dotenv
from loader.buildPatient import build_patient
from loader.handleBio import handleBio
from loader.handleHem import handleHem
from loader.handlePat import handlePatolog
from loader.handlePatientData import handlePatientData
from model.seriliaziePatient import savePatient
# Load environment variables
load_dotenv()

class DatabaseLoader:
    def __init__(self):
        """Initialize database connection parameters"""
        self.db_params = {
            'dbname': os.getenv('DB_NAME'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD'),
            'host': os.getenv('DB_HOST'),  # This can be an IP address
            'port': os.getenv('DB_PORT', '5432'),  # Default PostgreSQL port
            'connect_timeout': int(os.getenv('DB_CONNECT_TIMEOUT', '10')),  # Connection timeout in seconds
            # 'sslmode': os.getenv('DB_SSL_MODE', 'require'),  # SSL mode for secure connection
            'application_name': 'data_loader'  # Identify this connection in the database
        }
        self.conn = None
        self.cursor = None

    def connect(self):
        """Establish connection to the database"""
        try:
            print(f"Attempting to connect to database at {self.db_params['host']}:{self.db_params['port']}")
            self.conn = psycopg2.connect(**self.db_params)
            self.cursor = self.conn.cursor()
            print("Successfully connected to the database")
            
            # Print connection information
            self.cursor.execute("SELECT version();")
            db_version = self.cursor.fetchone()
            print(f"Connected to: {db_version[0]}")
            
        except Exception as e:
            print(f"Error connecting to database: {e}")
            raise

    def disconnect(self):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
            print("Database connection closed")

    def get_tables(self) -> List[str]:
        """Get list of all tables in the database"""
        query = """
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        """
        self.cursor.execute(query)
        return [row[0] for row in self.cursor.fetchall()]

    def load_data_by_cispac(self, cispac_value: str) -> Dict[str, pd.DataFrame]:
        """
        Load data from all tables where cispac column matches the given value
        
        Args:
            cispac_value: The cispac value to filter by
            
        Returns:
            Dictionary with table names as keys and pandas DataFrames as values
        """
        if not self.conn or not self.cursor:
            self.connect()

        tables = self.get_tables()
        results = {}

        for table in tables:
            try:
                # Check if table has cispac column
                self.cursor.execute(f"""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name = '{table}' 
                    AND column_name = 'cispac'
                """)
                
                if self.cursor.fetchone():
                    # Table has cispac column, fetch data
                    query = sql.SQL("SELECT * FROM {} WHERE cispac = %s").format(
                        sql.Identifier(table)
                    )
                    self.cursor.execute(query, (cispac_value,))
                    
                    # Get column names
                    colnames = [desc[0] for desc in self.cursor.description]
                    
                    # Fetch all rows
                    rows = self.cursor.fetchall()
                    
                    # Create DataFrame
                    if rows:
                        df = pd.DataFrame(rows, columns=colnames)
                        results[table] = df
                        print(f"Loaded {len(rows)} rows from {table}")
                    else:
                        print(f"No data found in {table} for cispac value {cispac_value}")
                        
            except Exception as e:
                print(f"Error loading data from {table}: {e}")
                continue

        return results

def main():
    # Example usage
    loader = DatabaseLoader()
    cispac_value = "YOUR_CISPAC_VALUE"  # Replace with actual cispac value
    try:
        loader.connect()
        results = loader.load_data_by_cispac(cispac_value)
        
        # Process results
        for table_name, df in results.items():
            print(f"\nData from {table_name}:")
            print(df.head())
            
        patient = build_patient(results, cispac_value)

        for table_name, df in results.items():
            if table_name == "LabBio":
                handleBio(df, patient)
            elif table_name == "LabHem":
                handleHem(df, patient)
            elif table_name == "Patolog":
                handlePatolog(df, patient)
            elif table_name == "Pacient":
                handlePatientData(df, patient)
        
        savePatient(f"patient_{cispac_value}.json", patient)
          
    
    except Exception as e:
        print(f"Error: {e}")
    finally:
        loader.disconnect()

if __name__ == "__main__":
    main()
