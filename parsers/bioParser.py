import os
import pandas as pd
from parsers.utils import pathTo

BASE_PATH = pathTo("data/DATA") # years gets filled in


def parseFile(file: str) -> pd.DataFrame:
    """
    Parses a single file of reports and returns a list of parsed data
    """

    df = pd.read_csv(
        file,
        quotechar='"',
        skipinitialspace=True,
        dtype=str,  # Read everything as string to avoid parsing issues
    )


    # Remove rows where all values are empty
    def to_float(val):
        try:
            return float(val.replace(',', '.').replace('<', '').replace('!', '').replace('*', '').strip())
        except:
            return None

    # df['VALNUM'] = pd.to_numeric(df['VALNUM'], errors='coerce')
    # df['VALTXT_CLEAN'] = df['VALTXT'].apply(lambda x: to_float(x) if pd.notnull(x) else None)

    return df


def parse() -> pd.DataFrame:
    """
    Parses all files that are for this parser and returns a list of parsed data
    It should use parseFile to parse each file to avoid code duplication

    "ORDNUM",
    "DAYNUM"
    "ORDDATE"
    "CISPAC"
    "SEX"
    "DEPARTM"
    "DG1"
    "DG2"
    "DG3"
    "DG4"
    "DG5"
    "DGTXT"
    "ENTRYDATE"
    "HEIGHT"
    "WEIGHT"
    "METD"
    "VALNUM"
    "VALTXT"
    "VALLIMIT"
    "VALCOMMENT"
    "VALDESCR"
    "MACHINE"
    """
    print("PARSING BIO DATA")
    df = pd.DataFrame()
    for year in [23, 24]:
        dir = BASE_PATH / f"LAB_{year}"
        for file in os.listdir(dir):
            if file.startswith("BIO") and file.endswith(".csv"):
                print(f"Parsing file: {file}")
                temp_df = parseFile(dir / file)
                df = pd.concat([df, temp_df])
            else:
                print(f"Skipping file: {file}")

    df = df.dropna(axis=1, how='all')
    # Remove rows where CISPAC is 0, missing, or invalid
    df = df[df['CISPAC'].apply(lambda x: x.isdigit() and int(x) != 0 if pd.notnull(x) else False)]

    return df


if __name__ == "__main__":
    df = parse()
    print(df.info())
    print(df.head(10))

