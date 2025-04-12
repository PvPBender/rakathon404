#!/usr/bin/env python

import os
import pandas as pd
import datetime  # Add this import for timestamp

# Updated paths for RTG data
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) # Adjust PROJECT_ROOT to point to rakathon404
BASE_PATH = os.path.join(PROJECT_ROOT, 'data', 'DATA', 'RTG', '$Rentgen202504101118.csv')
RTG_DATA_DIR = os.path.join(PROJECT_ROOT, 'data', 'DATA', 'RTG', 'Data') # Directory containing the .data files

# Generate timestamp for the output file
timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
OUTPUT_PATH = os.path.join(PROJECT_ROOT, 'data', 'DATA', 'RTG', f'rtgParsed_{timestamp}.csv') # Output with timestamp

def read_data_file(file_path_in_col):
    """
    Reads the content of a data file specified by a path in a DataFrame column.
    Assumes the actual data files are located in RTG_DATA_DIR.
    Tries multiple encodings.
    """
    if pd.isna(file_path_in_col) or not isinstance(file_path_in_col, str) or not file_path_in_col.strip():
        return None

    try:
        # Extract only the filename from the potentially incorrect path in the column
        filename = os.path.basename(file_path_in_col)
        if not filename:
            return None

        # Construct the correct path to the data file
        actual_file_path = os.path.join(RTG_DATA_DIR, filename)

        if not os.path.exists(actual_file_path):
            # print(f"Warning: Data file not found: {actual_file_path}") # Optional warning
            return None

        # Try reading with different encodings
        encodings_to_try = ['cp1250', 'utf-8']
        for enc in encodings_to_try:
            try:
                with open(actual_file_path, 'r', encoding=enc) as f:
                    return f.read()
            except UnicodeDecodeError:
                continue
            except Exception as e:
                # print(f"Error reading {actual_file_path} with {enc}: {e}") # Optional warning
                return f"Error reading file: {e}" # Return error message if read fails after trying encodings

        # If all encodings fail
        # print(f"Warning: Could not decode file {actual_file_path} with tried encodings.") # Optional warning
        return "Error: Could not decode file"

    except Exception as e:
        # print(f"Error processing path {file_path_in_col}: {e}") # Optional warning
        return f"Error processing path: {e}"


def parse():
    """
    Parses the RTG CSV file, reads linked data files specified in the 'POPIS' column,
    and saves the combined data to a new CSV file.
    """
    if not os.path.exists(BASE_PATH):
        raise FileNotFoundError(f"Input CSV file not found at: {BASE_PATH}")

    if not os.path.exists(RTG_DATA_DIR):
         print(f"Warning: Data directory not found at: {RTG_DATA_DIR}. Content linking will fail.")
         # Decide if you want to raise an error or continue without linking
         # raise FileNotFoundError(f"Data directory not found at: {RTG_DATA_DIR}")


    # Try to load the file with different encodings
    df = None
    encodings_tried = ['windows-1250', 'ISO-8859-1', 'utf-8']
    for enc in encodings_tried:
        try:
            # Assuming the CSV uses comma as separator and double quotes for quoting
            df = pd.read_csv(BASE_PATH, encoding=enc, low_memory=False, sep=',', quotechar='"')
            print(f"Successfully read CSV with encoding: {enc}")
            break # Stop trying once successful
        except UnicodeDecodeError:
            print(f"Failed to read CSV with encoding: {enc}")
            continue
        except Exception as e:
            print(f"Error reading CSV file {BASE_PATH} with encoding {enc}: {e}")
            # Continue to try next encoding or raise error if needed

    if df is None:
         raise ValueError(f"Could not read CSV file {BASE_PATH} with any of the tried encodings: {encodings_tried}")


    # Ensure the POPIS column exists
    if "POPIS" not in df.columns:
        print("Warning: 'POPIS' column not found in the CSV. Cannot link data files.")
        df['RTG_DATA_CONTENT'] = None # Add empty column if POPIS is missing
    else:
         # Apply the function to create the new column with data file content
         print(f"Linking and reading data files from {RTG_DATA_DIR} based on 'POPIS' column...")
         df['RTG_DATA_CONTENT'] = df['POPIS'].apply(read_data_file)
         print("Finished reading data files.")

    # Ensure output directory exists
    output_dir = os.path.dirname(OUTPUT_PATH)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")

    # Save the processed DataFrame
    df.to_csv(OUTPUT_PATH, index=False, encoding='utf-8')
    print(f"\nParsed {len(df)} rows. Saved parsed data with linked content to: {OUTPUT_PATH}")
    return df


if __name__ == "__main__":
    try:
        print(f"Reading RTG CSV file from: {BASE_PATH}")
        df_parsed = parse()
        print("\nDataFrame Info:")
        df_parsed.info()
        print("\nFirst 5 rows of parsed data:")
        print(df_parsed.head())
        # Check content of the new column for a few rows where POPIS might be present
        print("\nSample of linked data content (first 5 non-empty):")
        # Ensure the column exists before trying to access it
        if 'RTG_DATA_CONTENT' in df_parsed.columns:
            print(df_parsed[df_parsed['RTG_DATA_CONTENT'].notna()]['RTG_DATA_CONTENT'].head())
        else:
            print("RTG_DATA_CONTENT column was not created (likely POPIS column missing).")


    except FileNotFoundError as e:
        print(f"Error: {e}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
