import pandas as pd
import logging
import numpy as np
from add_typ_lecby import annotate_vykony_with_names


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)


def load_and_prepare_data(year):
    """
    Loads and preprocesses data files for the given year from the directory `data/DATA/VYK_{year}/`.

    The function performs the following steps:
    - Loads CSV files 'material', 'vykony', and 'vykpac' using cp1250 encoding and `;` as the delimiter.
    - Strips whitespace from identifier columns (`CISPAC`, `CDOKL`, `KOD`).
    - Converts the 'DATUM' column to datetime format and logs any conversion errors.
    - Attempts to automatically convert `object` columns to numeric types; otherwise, strips whitespace.
    - Merges `vykony` and `material` data with `vykpac` based on the `CDOKL` column.
    - Adds a `ROK` column containing the current year.

    Parameters:
    year (int): The year for which the data should be loaded and processed.

    Returns:
    tuple: (df_vykony_full, df_material_full) – the merged and preprocessed DataFrame objects,
           or `None` if loading fails.
    """

    path = f"data/DATA/VYK_{year}/"
    material_path = path + f"vyk_{year}_material.csv"
    vykony_path = path + f"vyk_{year}_vykony.csv"
    vykpac_path = path + f"vyk_{year}_vykpac.csv"

    logging.info(f"[{year}] Načítám soubory...")
    try:
        df_material = pd.read_csv(material_path, sep=";", encoding="cp1250")
        logging.info(f"[{year}] Soubor 'material' načten: {df_material.shape}")
    except Exception as e:
        logging.error(f"[{year}] Chyba při načítání material: {e}")
        df_material = None

    try:
        df_vykony = pd.read_csv(vykony_path, sep=";", encoding="cp1250",
                                low_memory=False)
        logging.info(f"[{year}] Soubor 'vykony' načten: {df_vykony.shape}")
    except Exception as e:
        logging.error(f"[{year}] Chyba při načítání vykony: {e}")
        df_vykony = None

    try:
        df_vykpac = pd.read_csv(vykpac_path, sep=";", encoding="cp1250",
                                low_memory=False)
        logging.info(f"[{year}] Soubor 'vykpac' načten: {df_vykpac.shape}")
    except Exception as e:
        logging.error(f"[{year}] Chyba při načítání vykpac: {e}")
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
            df["DATUM"] = pd.to_datetime(df["DATUM"], dayfirst=True,
                                         errors="coerce")
            n_missing = df["DATUM"].isna().sum()
            if n_missing > 0:
                logging.warning(
                    f"[{year}] {name}: {n_missing} hodnot DATUM nebylo možné převést.")

    def auto_convert_object_columns(df, name=""):
        logging.info(f"[{year}] Převádím object sloupce v tabulce '{name}'...")
        for col in df.columns:
            if df[col].dtype == "object":
                try:
                    df[col] = pd.to_numeric(df[col], errors="coerce")
                    if df[col].notna().sum() == 0:
                        df[col] = df[col].astype(str).str.strip()
                except Exception:
                    df[col] = df[col].astype(str).str.strip()
        logging.info(f"[{year}] Převod dokončen pro tabulku '{name}'.")

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
    """
    Removes columns from the DataFrame that are entirely empty.

    Empty values are defined broadly to include standard missing value indicators
    like empty strings, 'NULL', 'n/a', etc. These are replaced with np.nan,
    and then columns that contain only np.nan are dropped.

    Parameters:
    df (pd.DataFrame): The input DataFrame to clean.
    name (str): A name identifier for logging purposes.

    Returns:
    pd.DataFrame: The cleaned DataFrame with empty columns removed.
    """
    n_cols_before = df.shape[1]

    null_equivalents = ["", " ", "  ", "<null>", "NULL", "N/A", "n/a", "None",
                        "nan", "NaN"]
    df_cleaned = df.replace(null_equivalents, np.nan).infer_objects(copy=False)

    df_cleaned = df_cleaned.dropna(axis=1, how="all")

    n_removed = n_cols_before - df_cleaned.shape[1]
    logging.info(f"Table '{name}': removed {n_removed} empty columns.")

    return df_cleaned


df_vykony_23, df_material_23 = load_and_prepare_data(23)
df_vykony_24, df_material_24 = load_and_prepare_data(24)


df_vykony_23 = drop_empty_columns(df_vykony_23, "vykony_23")
df_vykony_24 = drop_empty_columns(df_vykony_24, "vykony_24")
df_material_23 = drop_empty_columns(df_material_23, "material_23")
df_material_24 = drop_empty_columns(df_material_24, "material_24")


df_vykony_all = pd.concat([df_vykony_23, df_vykony_24], ignore_index=True)
df_material_all = pd.concat([df_material_23, df_material_24],
                            ignore_index=True)
df_vykony_all = annotate_vykony_with_names(df_vykony_all)
df_material_all = annotate_vykony_with_names(df_material_all)
