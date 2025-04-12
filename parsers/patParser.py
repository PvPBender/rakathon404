#!/usr/bin/env python
import os
import pandas as pd
from parsers.utils import readFile, pathTo

OUTPUT_PATH = pathTo('parsers', 'parsed', 'PAT')
BASE_PATH = pathTo('data','DATA','PAT')

NUM_COLS = 22  # We expect 22 columns => 21 commas

def clean_datetime_columns(df: pd.DataFrame, datetime_columns: list) -> pd.DataFrame:
    """
    Cleans datetime columns by ensuring the correct datetime format for MySQL.
    """
    for col in datetime_columns:
        if col in df.columns:
            # Convert to datetime and format as 'YYYY-MM-DD HH:MM:SS'
            df[col] = pd.to_datetime(df[col], errors='coerce').dt.strftime('%Y-%m-%d %H:%M:%S')
    return df

def parse_csv_char_by_char(data, expected_num_cols):
    rows = []
    current_row = []
    current_field = []

    in_quotes = False
    i = 0
    length = len(data)

    while i < length:
        ch = data[i]
        if ch == '"':
            # Look ahead for escaped quote ("")
            if in_quotes and i + 1 < length and data[i + 1] == '"':
                # It's an escaped double quote, add a single " to field
                current_field.append('"')
                i += 2
                continue
            else:
                # Just toggle
                in_quotes = not in_quotes
                i += 1
                continue

        # If we encounter a comma *outside* quotes, that's the end of a field
        if ch == ',' and not in_quotes:
            current_row.append(''.join(current_field).strip())
            current_field = []
            i += 1
            continue

        # If we see a newline *outside* quotes, that’s the end of the record
        if (ch == '\n' or ch == '\r') and not in_quotes:
            # Finalize the last field in this row
            current_row.append(''.join(current_field).strip())
            current_field = []

            # If the row has the correct # of columns, we accept it
            if len(current_row) == expected_num_cols:
                rows.append(current_row)
            else:
                # If the row does not have the correct # of columns, skip or handle differently
                pass

            current_row = []
            # skip over possible Windows \r\n
            i += 1
            continue

        # Otherwise, just accumulate the character
        current_field.append(ch)
        i += 1

    # If data does not end with a newline, handle a final partial row
    if current_field or current_row:
        current_row.append(''.join(current_field).strip())
        if len(current_row) == expected_num_cols:
            rows.append(current_row)

    return rows

def parseFile(file: str, fileName: str | None):
    """
    Parses all files that are for this parser and returns a list of parsed data
    It should use parseFile to parse each file to avoid code duplication
    
    - SUBSYSTEM: Subsystem
    - ROK: Year
    - CISLOSUB: Cislo subjektu
    - POHLAVI
    - DATUM: datum zalozeni
    - DATUMVYSL: datum vysledku
    - ODDEL: oddeleni
    - DG: Diagnoza
    - DG1: Diagnoza
    - LOKAL1: Lokalizace
    - LOKAL2: Lokalizace
    - LOKAL3: Lokalizace
    - DGPAT: diagonoza patologie
    - TYPVZORKU: Typ vzorku
    - IDZAD: Identifikator zadatele
    - CISPAC: Cislo pacienta    
    - DODATEK: Dodatek
    - DODATEK1: Dodatek
    - PRILOHA: Priloha
    - PRILOHA1: Priloha
    - KLINDG: Klinicka diagnnoza - slovni popis
    - TEXT: slovni popis vysetreni
    """
    if not os.path.exists(OUTPUT_PATH):
        os.makedirs(OUTPUT_PATH)

    # Read the entire file lines
    all_lines = readFile(file).splitlines()
    if not all_lines:
        raise ValueError("File is empty; no data found.")

    header_line = all_lines[0]
    columns = []
    in_quotes = False
    field = []
    for c in header_line:
        if c == '"':
            in_quotes = not in_quotes
        elif c == ',' and not in_quotes:
            columns.append(''.join(field).strip().replace('"', ''))
            field = []
        else:
            field.append(c)
    columns.append(''.join(field).strip().replace('"', ''))

    if len(columns) != NUM_COLS:
        raise ValueError(f"Header row does not have the expected {NUM_COLS} columns. "
                         f"Found {len(columns)}: {columns}")
    data_block = "\n".join(all_lines[1:])  # join the rest of the lines
    records = parse_csv_char_by_char(data_block, NUM_COLS)
    df = pd.DataFrame(records, columns=columns)
    df = df.replace(r'[\r\n]+', ' ', regex=True)

    print("Cleaning date time columns...")
    datetime_columns = ['DATUM', 'DATUMVYSL']
    df = clean_datetime_columns(df, datetime_columns)

    
    if "TEXT" in df.columns:
        df["TEXT"] = df["TEXT"].str.replace(r'[\r\n\u2028\u2029]+', ' ', regex=True)
        df["TEXT"] = df["TEXT"].str.replace(r'[\r\n\u2028\u2029\x00-\x1F\x7F-\x9F\t]+', ' ', regex=True)

    outPath = os.path.join(OUTPUT_PATH, os.path.basename(file).removeprefix("$"))
    df.to_csv(outPath, index=False, encoding='utf-8')
    print(f"\nParsed {len(df)} rows. Saved parsed data to: {outPath}")

    return df

def parse() -> pd.DataFrame:
    """"
    Parses all files in a directory
    """
    df = pd.DataFrame()
    for file in os.listdir(BASE_PATH):
        if "pat" in file.lower():
            print(f"Parsing file: {file}")
            parsed = parseFile(os.path.join(BASE_PATH, file), file)
            df = pd.concat([df, parsed])
        else:
            print(f"Skipping file: {file}")

    return df 

if __name__ == "__main__":
    # try:
    df = parseFile(os.path.join(BASE_PATH, "$PATOL202504101802.csv"), None)
    print(f"Reading file from: {BASE_PATH}")
    print(df.head(12))
    print("\nDataFrame Info:")
    print(df.info())
    # except Exception as e:
    #     print("Error parsing:", e)
