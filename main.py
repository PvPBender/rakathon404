from db.database import connect

from parsers import ambulanceMessage, releaseMessage, patParser, rtgParser, vykParser, bioParser, hemParser

import db.tables 

if __name__ == "__main__":
    # Connect to the database
    connection, engine = connect()
    db.tables.Base.metadata.create_all(engine)

    patDF = patParser.parse()
    db.tables.Patolog.insert(patDF)
    
    # Check if the connection was successful
    if connection:
        # Perform database operations here

        # Close the connection when done
        connection.close()