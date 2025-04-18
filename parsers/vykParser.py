from typing import Tuple
import pandas as pd
import numpy as np
import logging
import requests
import os
from parsers.utils import pathTo, clean_datetime_columns
from parsers.VYK.add_typ_lecby import annotate_vykony_with_names

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

OUTPUT_PATH = pathTo('parsers/parsed')


def get_data_paths(year):
    base_path = pathTo("data", "DATA", f"VYK_{year}")
    
    material_path = base_path / f"vyk_{year}_material.csv"
    vykony_path = base_path / f"vyk_{year}_vykony.csv"
    vykpac_path = base_path / f"vyk_{year}_vykpac.csv"
    return material_path, vykony_path, vykpac_path


def load_and_prepare_data(year):
    material_path, vykony_path, vykpac_path = get_data_paths(year)

    logging.info(f"[{year}] Loading files...")
    try:
        df_material = pd.read_csv(material_path, sep=";", encoding="cp1250")
        logging.info(f"[{year}] File 'material' loaded: {df_material.shape}")
    except Exception as e:
        logging.error(f"[{year}] Error while loading 'material': {e}")
        df_material = None

    try:
        df_vykony = pd.read_csv(vykony_path, sep=";", encoding="cp1250",
                                low_memory=False)
        logging.info(f"[{year}] File 'vykony' loaded: {df_vykony.shape}")
    except Exception as e:
        logging.error(f"[{year}] Error while loading 'vykony': {e}")
        df_vykony = None

    try:
        df_vykpac = pd.read_csv(vykpac_path, sep=";", encoding="cp1250",
                                low_memory=False)
        logging.info(f"[{year}] File 'vykpac' loaded: {df_vykpac.shape}")
    except Exception as e:
        logging.error(f"[{year}] Error while loading 'vykpac': {e}")
        df_vykpac = None

    def clean_ids(df, cols):
        for col in cols:
            df[col] = df[col].astype(str).str.replace(r"\s+", "", regex=True)
        return df

    if df_material is not None:
        df_material = clean_ids(df_material, ["CISPAC", "CDOKL", "KOD"])
    if df_vykony is not None:
        df_vykony = clean_ids(df_vykony, ["CISPAC", "CDOKL", "KOD"])
    if df_vykpac is not None:
        df_vykpac = clean_ids(df_vykpac, ["CISPAC", "CDOKL"])

    for name, df in zip(["material", "vykony"], [df_material, df_vykony]):
        if df is not None:
            df = clean_datetime_columns(df, ["DATUM"])
            
            n_missing = df["DATUM"].isna().sum()
            if n_missing > 0:
                logging.warning(
                    f"[{year}] {name}: {n_missing} values of DATE could not be converted.")

    def auto_convert_object_columns(df, name=""):
        logging.info(
            f"[{year}] Converting object columns in table '{name}'...")
        for col in df.columns:
            if df[col].dtype == "object":
                try:
                    df[col] = pd.to_numeric(df[col], errors="coerce")
                    if df[col].notna().sum() == 0:
                        df[col] = df[col].astype(str).str.strip()
                except Exception:
                    df[col] = df[col].astype(str).str.strip()
        logging.info(f"[{year}] Conversion completed for table '{name}'.")

    if df_material is not None:
        auto_convert_object_columns(df_material, "material")
    if df_vykony is not None:
        auto_convert_object_columns(df_vykony, "vykony")
    if df_vykpac is not None:
        auto_convert_object_columns(df_vykpac, "vykpac")

    if df_vykony is not None and df_vykpac is not None:
        df_vykony_full = df_vykony.merge(
            df_vykpac[["CDOKL", "CISPAC"]],
            on="CDOKL",
            how="left",
            suffixes=("", "_Z_UCTU")
        )
        df_vykony_full["ROK"] = year
    else:
        df_vykony_full = None

    if df_material is not None and df_vykpac is not None:
        df_material_full = df_material.merge(
            df_vykpac[["CDOKL", "CISPAC"]],
            on="CDOKL",
            how="left",
            suffixes=("", "_Z_UCTU")
        )
        df_material_full["ROK"] = year
    else:
        df_material_full = None

    return df_vykony_full, df_material_full


def drop_empty_columns(df, name):
    null_equivalents = ["", " ", "  ", "<null>", "NULL", "N/A", "n/a", "None",
                        "nan", "NaN"]
    df_cleaned = df.replace(null_equivalents, np.nan).infer_objects(copy=False)
    n_cols_before = df.shape[1]
    df_cleaned = df_cleaned.dropna(axis=1, how="all")
    n_removed = n_cols_before - df_cleaned.shape[1]
    logging.info(f"Table '{name}': removed {n_removed} empty columns.")
    return df_cleaned


CUR_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = pathTo("parsers/parsed/VYK")  # Uprav dle potřeby


def extract_codes_names_from_url_to_csv(url: str, csv_path: str) -> None:
    """
    Downloads an Excel file from a URL, reads it, and saves it as a CSV.
    """

    response = requests.get(url)
    response.raise_for_status()

    with open(os.path.join(CUR_DIR, "temp.xlsx"), "wb") as f:
        f.write(response.content)

    df = pd.read_excel(os.path.join(CUR_DIR, "temp.xlsx"))
    df.to_csv(csv_path, index=False)

    os.remove(os.path.join(CUR_DIR, "temp.xlsx"))


def parse() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Parses all files that are for this parser and returns a list of parsed data.
    returns Tuple of DataFrames: (df_vykony_annotated, df_material_all)
    """

    csv_path = pathTo("parsers/VYK/vykony_kody_nazvy.csv")
    vyhlaska_url = "https://szv.mzcr.cz/Vykon/Data/Vyhlaska.xlsx"

    if not os.path.exists(csv_path):
        extract_codes_names_from_url_to_csv(vyhlaska_url, csv_path)

    df_vykony_all = pd.DataFrame()
    df_material_all = pd.DataFrame()

    for year in [23, 24]:
        df_vykony, df_material = load_and_prepare_data(year)

        df_vykony = drop_empty_columns(df_vykony, f"vykony_{year}")
        df_material = drop_empty_columns(df_material, f"material_{year}")

        df_vykony_all = pd.concat([df_vykony_all, df_vykony],
                                  ignore_index=True)
        df_material_all = pd.concat([df_material_all, df_material],
                                    ignore_index=True)

    os.makedirs(OUTPUT_PATH, exist_ok=True)

    df_vykony_annotated = annotate_vykony_with_names(
        vykony_csv_or_df=df_vykony_all,
        kod_ciselnik=csv_path,
        output_csv=OUTPUT_PATH / "vykony_annotated.csv"
    )

    df_material_all.to_csv(OUTPUT_PATH / "material_all.csv", index=False)

    return df_vykony_annotated, df_material_all

def getParsed() -> Tuple[pd.DataFrame, pd.DataFrame]:
    df_annotated = pd.read_csv(OUTPUT_PATH / "vykony_annotated.csv")
    df_material = pd.read_csv(OUTPUT_PATH / "material_all.csv")

    return df_annotated, df_material

if __name__ == "__main__":
    parse()
