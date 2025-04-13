from db.database import connect

from parsers import ambulanceMessage, releaseMessage, patParser, rtgParser, vykParser, bioParser, hemParser
from parsers.utils import pathTo


import db.tables 
import pandas as pd

# vykParser.parse()
# ambulanceMessage.parse()
# releaseMessage.parse()
# rtgParser.parse()
# bioParser.parse()
# hemParser.parse()


if __name__ == "__main__":
    # Connect to the database
    connection, engine = connect()
    db.tables.Base.metadata.create_all(engine)
    
    # df = pd.read_csv(pathTo("parsers/parsed/LAB/hem.csv"))#hemParser.parse()
    # db.tables.HemLab.insert(df)

    # df = bioParser.parse() # pd.read_csv(pathTo("parsers/parsed/LAB/bio.csv"))# 
    # db.tables.BioLab.insert(df)

    # df = pd.read_csv(pathTo("parsers/parsed/PAT/PATOL202504101802.csv")) #patParse.parse()
    # db.tables.Patolog.insert(df)

    # df = ambulanceMessage.parse()
    # db.tables.Report.insert(df, db.tables.ReportType.AmbulanceReport)

    # df = releaseMessage.parse()
    # db.tables.Report.insert(df, db.tables.ReportType.ReleaseReport)

    # df = rtgParser.parse() # pd.read_csv(pathTo("parsers/parsed/RTG/Rentgen202504101118.csv")) # 
    # db.tables.Rentgen.insert(df)

    # df_anot, df_mat = vykParser.parse() # vykParser.parse() #
    # db.tables.AnnotatedPerformance.insert(df_anot)
    # db.tables.HospitalReport.insert(df_mat)
    
    # Check if the connection was successful
    if connection:
        # Perform database operations here

        # Close the connection when done
        connection.close()