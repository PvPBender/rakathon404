import os
import sys

# Add the project root to Python's path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from parsers import patParser
import pandas as pd
import logging
import loader.handlePat as handlePat
from loader.buildPatient import build_patient


PARSED_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "data", "pat", "PATOL_parsed.csv")


def main():
    if not os.path.exists(PARSED_PATH):
        logging.error("PATOL_parsed.csv does not exist")
        patParser.parse()

    patient = build_patient(1)

    with open(PARSED_PATH, "r") as file:
        for line in file:
            handlePat.handlePat(line, patient)
            break
    
if __name__ == "__main__":
    main()