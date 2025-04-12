import pandas as pd
import logging
import sys
import os


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("../../extract_codes_names.log", mode='w', encoding='utf-8')
    ]
)

file_path = "../../data/Vyhlaska.xlsx"
output_path = "vykony_kody_nazvy.csv"

# Ensure output directory exists
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Check output path
if os.path.isdir(output_path):
    logging.error(f"'{output_path}' is a directory. Please provide a file name.")
    sys.exit(1)

try:
    logging.info(f"Loading Excel file: {file_path}")
    excel_data = pd.read_excel(file_path, sheet_name=None)
except ImportError:
    logging.error("Missing 'openpyxl'. Install it with: pip install openpyxl")
    raise
except Exception:
    logging.exception("Failed to load the Excel file.")
    raise

try:
    df = excel_data['test']
    df.columns = [f"col_{i}" for i in range(len(df.columns))]

    def is_code(val):
        try:
            return pd.notna(val) and str(val).strip().isdigit()
        except:
            return False

    def is_valid_name(val):
        return isinstance(val, str) and val.strip() != ""

    # Filter valid rows
    filtered_df = df[
        df['col_0'].apply(is_code) &
        df['col_1'].apply(is_valid_name)
    ].copy()

    # Convert code to integer
    filtered_df['col_0'] = filtered_df['col_0'].astype(int)

    # Select and rename columns
    filtered_df = filtered_df[['col_0', 'col_1']]
    filtered_df.columns = ['code', 'name']

    # Save result
    filtered_df.to_csv(output_path, index=False)
    logging.info(f"Data successfully saved to: {output_path}")
    logging.info(f"Extracted {len(filtered_df)} valid performance records.")

except KeyError:
    logging.error("Sheet 'test' not found.")
    raise
except Exception:
    logging.exception("Error during processing.")
    raise


