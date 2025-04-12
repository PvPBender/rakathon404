#!/usr/bin/env python

import os
import pandas as pd
import datetime
import logging
from parsers.utils import pathTo, clean_datetime_columns



# Define the path for the output CSV file, including a timestamp.
# Example format: rtgParsed_YYYYMMDDHHMMSS.csv
# timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


BASE_PATH = pathTo('data', 'DATA', 'RTG')
RTG_DATA_DIR = pathTo('data', 'DATA', 'RTG', 'Data') # Directory containing the actual RTG data files (referenced in the main CSV).
OUTPUT_PATH = pathTo('parsers', 'parsed', 'RTG')


# --- Functions ---

def read_data_file(file_path_in_col: str) -> str | None:
    """
    Reads the content of an external data file referenced in the main CSV.

    Handles potentially malformed paths stored in the DataFrame column,
    constructs the correct path within RTG_DATA_DIR, and attempts to read
    the file using multiple encodings.

    Args:
        file_path_in_col: The raw file path string from the DataFrame column.

    Returns:
        - str: The content of the file if successfully read.
        - None: If the input path is invalid, empty, NaN, or the file doesn't exist.
        - str: An error message string if reading fails (e.g., encoding issues, permissions).
    """
    # Basic validation for the input path string
    if pd.isna(file_path_in_col) or not isinstance(file_path_in_col, str) or not file_path_in_col.strip():
        return None

    try:
        # Extract filename assuming the path in the column might be incorrect/absolute
        filename = os.path.basename(file_path_in_col)
        if not filename: # Handle cases where basename extraction fails
            return None

        # Construct the expected full path to the data file within RTG_DATA_DIR
        actual_file_path = os.path.join(RTG_DATA_DIR, filename)

        # Check if the constructed file path actually exists
        if not os.path.exists(actual_file_path):
            # logging.warning(f"Data file not found: {actual_file_path}") # Optional: Log missing files
            return None

        # Attempt to read the file using common encodings for this data type
        encodings_to_try = ['cp1250', 'utf-8'] # cp1250 for outdated Czech encodings
        for enc in encodings_to_try:
            try:
                with open(actual_file_path, 'r', encoding=enc) as f:
                    return f.read() # Return content on successful read
            except UnicodeDecodeError:
                continue # Try the next encoding if decoding fails
            except Exception as e:
                logging.warning(f"Error reading {actual_file_path} with {enc}: {e}")
                return f"Error reading file: {e}" # Return specific error

        # If all specified encodings fail
        logging.warning(f"Could not decode file {actual_file_path}.")
        return "Error: Could not decode file"

    except Exception as e:
        # Catch any other unexpected errors during path processing or file access
        logging.error(f"Error processing path '{file_path_in_col}': {e}")
        return f"Error processing path: {e}"



def parseFile(file: str, fileName: str | None) -> list[str]:
    """
    Parses the main RTG CSV file, links associated data file content, and saves the result.

    Reads the CSV specified by BASE_PATH, uses the 'POPIS' column to find
    corresponding data files in RTG_DATA_DIR, reads their content using
    `read_data_file`, adds this content to a new 'RTG_DATA_CONTENT' column,
    and saves the resulting DataFrame to a timestamped CSV file specified by OUTPUT_PATH.

    Returns:
        pd.DataFrame: The DataFrame containing the original CSV data plus the
                      linked content from external files in the 'RTG_DATA_CONTENT' column.

    Raises:
        FileNotFoundError: If the main input CSV (BASE_PATH) is not found.
        ValueError: If the main input CSV cannot be read using any of the attempted encodings.
        # Note: FileNotFoundError for RTG_DATA_DIR is handled with a warning, not an exception.
    """
    df = None
    try:
        # Use pandas to read the CSV, specifying separator and quote character.
        # low_memory=False can help with mixed data types but uses more memory.
        df = pd.read_csv(file, encoding='windows-1250', low_memory=False, sep=',', quotechar='"')
        df.drop(columns=["CISPAC"], inplace=True)
        df.rename(columns={'CISPAC.1': 'CISPAC'}, inplace=True)
        
        print("Cleaning date time columns...")
        datetime_columns = ['DATUM', "VYSLDAT"]
        df = clean_datetime_columns(df, datetime_columns)

    except UnicodeDecodeError:
        raise ValueError(f"Failed to read CSV {file} with encoding windows-1250")
    except Exception as e:
        raise ValueError(f"Could not read CSV file {file} due to: {e}")

    # --- Link External Data ---
    # Check if the 'POPIS' column (expected to contain file paths) exists.
    if "POPIS" not in df.columns:
        logging.warning("'POPIS' column not found in the CSV. Cannot link external data files.")
        df['RTG_DATA_CONTENT'] = None # Add an empty column for consistency if POPIS is missing
    else:
        # Apply the read_data_file function to each entry in the 'POPIS' column.
        logging.info(f"Linking and reading data files from {RTG_DATA_DIR} based on 'POPIS' column...")
        # This creates the new 'RTG_DATA_CONTENT' column with file contents or errors/None.
        df['RTG_DATA_CONTENT'] = df['POPIS'].apply(read_data_file)
        logging.info("Finished reading and linking external data files.")


    # --- Save Output ---
    if not os.path.exists(OUTPUT_PATH):
        os.makedirs(OUTPUT_PATH)
        logging.info(f"Created output directory: {OUTPUT_PATH}")

    # Write the final DataFrame (with linked data) to a new CSV file.
    df.to_csv(OUTPUT_PATH / fileName.removeprefix('$'), index=False, encoding='utf-8')
    logging.info(f"Parsed {len(df)} rows. Saved combined data to: {OUTPUT_PATH}")

    return df


def parse() -> pd.DataFrame:
    """"
    Parses all files in a directory
    """
    if not os.path.exists(RTG_DATA_DIR):
        logging.warning(f"Data directory not found at: {RTG_DATA_DIR}. Content linking will fail.")

    df = pd.DataFrame()
    for file in os.listdir(BASE_PATH):
        if "rentgen" in file.lower():
            print(f"Parsing file: {file}")
            parsed = parseFile(BASE_PATH / file, file)
            df = pd.concat([df, parsed])
        else:
            print(f"Skipping file: {file}")
    return df

# --- Main Execution ---
if __name__ == "__main__":
    """
    Entry point when the script is executed directly.
    Calls the main parse function and logs summary information.
    """
    try:
        logging.info(f"Starting RTG data parsing process...")
        logging.info(f"Reading main CSV from: {BASE_PATH}")
        df_parsed = parse() # Execute the parsing pipeline

        # --- Log Summary Information ---
        logging.info("--- Parsing Summary ---")
        logging.info(f"Total rows processed: {len(df_parsed)}")

        # Log basic DataFrame structure (columns, data types, non-null counts)
        logging.info("DataFrame Info:")
        # Capture df.info() output as it prints to stdout by default
        import io
        buffer = io.StringIO()
        df_parsed.info(buf=buffer)
        logging.info(buffer.getvalue())

        # Log the first few rows as a sample
        logging.info("First 5 rows of parsed data:")
        # Use to_string() for better formatting in logs
        logging.info("\n" + df_parsed.head().to_string())

        # Log a sample of the linked content, if the column exists
        logging.info("Sample of linked data content (first 5 non-empty/non-error):")
        if 'RTG_DATA_CONTENT' in df_parsed.columns:
            # Filter out None, empty strings, and error messages before taking head()
            valid_content = df_parsed[
                df_parsed['RTG_DATA_CONTENT'].notna() &
                (df_parsed['RTG_DATA_CONTENT'] != '') &
                (~df_parsed['RTG_DATA_CONTENT'].astype(str).str.startswith('Error'))
            ]['RTG_DATA_CONTENT']

            if not valid_content.empty:
                logging.info("\n" + valid_content.head().to_string())
            else:
                logging.info("No valid linked data content found in the sample.")
        else:
            logging.warning("RTG_DATA_CONTENT column was not created (likely 'POPIS' column was missing or empty).")

        logging.info("--- RTG data parsing process finished successfully ---")

    except FileNotFoundError as e:
        logging.error(f"Fatal Error: Required file not found. {e}")
    except ValueError as e:
        logging.error(f"Fatal Error: Data processing error. {e}")
    except Exception as e:
        # Catch any other unexpected exceptions during the process
        logging.error(f"Fatal Error: An unexpected error occurred during execution: {e}", exc_info=True) # Log traceback
