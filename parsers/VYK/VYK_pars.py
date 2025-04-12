import pandas as pd
import logging
import os
import numpy as np
from pathlib import Path
from parsers.VYK.add_typ_lecby import annotate_vykony_with_names
from parsers.VYK.extract_codes_names import extract_codes_names

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

OUTPUT_PATH = os.getcwd() + '/parsers/parsed/'


def get_data_paths(year):
    current_dir = Path(__file__).resolve().parent
    project_root = current_dir.parents[1]  # Správně: rakathon404/
    base_path = project_root / "data" / "DATA" / f"VYK_{year}"
    material_path = base_path / f"vyk_{year}_material.csv"
    vykony_path = base_path / f"vyk_{year}_vykony.csv"
    vykpac_path = base_path / f"vyk_{year}_vykpac.csv"
    return material_path, vykony_path, vykpac_path


def load_and_prepare_data(year):
    material_path, vykony_path, vykpac_path = get_data_paths(year)

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
    null_equivalents = ["", " ", "  ", "<null>", "NULL", "N/A", "n/a", "None",
                        "nan", "NaN"]
    df_cleaned = df.replace(null_equivalents, np.nan).infer_objects(copy=False)
    n_cols_before = df.shape[1]
    df_cleaned = df_cleaned.dropna(axis=1, how="all")
    n_removed = n_cols_before - df_cleaned.shape[1]
    logging.info(f"Table '{name}': removed {n_removed} empty columns.")
    return df_cleaned


# === main ===
def parse() -> list[any]:
    """
    Parses all files that are for this parser and returns a list of parsed data
    It should use parseFile to parse each file to avoid code duplication
    """


    if not os.path.exists("vykony_kody_nazvy.csv"):
        extract_codes_names(os.path.join(os.getcwd(), "parsers/VYK/Vyhlaska.xlsx"))
        
    df_vykony_all = pd.DataFrame()
    df_material_all = pd.DataFrame()

    for year in [23, 24]:
        df_vykony, df_material = load_and_prepare_data(year)

        df_vykony = drop_empty_columns(df_vykony, f"vykony_{year}")
        df_material = drop_empty_columns(df_material, f"material_{year}")

        df_vykony_all = pd.concat([df_vykony_all, df_vykony], ignore_index=True)
        df_material_all = pd.concat([df_material_all, df_material], ignore_index=True)

    
    
    df_vykony_annotated = annotate_vykony_with_names(
        vykony_csv_or_df=df_vykony_all,
        kod_ciselnik = "vykony_kody_nazvy.csv",#os.path.join(OUTPUT_PATH, "vykony_kody_nazvy.csv"),
        output_csv = os.path.join(OUTPUT_PATH, "vykony_annotated.csv")
    )

    file_path = os.path.join(OUTPUT_PATH, "material_all.csv")
    df_material_all.to_csv(file_path, index=False)

    return df_vykony_annotated




if __name__ == "__main__":
    parse()