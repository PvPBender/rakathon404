import pandas as pd
import logging
import os

# Nastavení logování
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def load_and_prepare_data(year):
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
        df_vykony = pd.read_csv(vykony_path, sep=";", encoding="cp1250", low_memory=False)
        logging.info(f"[{year}] Soubor 'vykony' načten: {df_vykony.shape}")
    except Exception as e:
        logging.error(f"[{year}] Chyba při načítání vykony: {e}")
        df_vykony = None

    try:
        df_vykpac = pd.read_csv(vykpac_path, sep=";", encoding="cp1250", low_memory=False)
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
            df["DATUM"] = pd.to_datetime(df["DATUM"], dayfirst=True, errors="coerce")
            n_missing = df["DATUM"].isna().sum()
            if n_missing > 0:
                logging.warning(f"[{year}] {name}: {n_missing} hodnot DATUM nebylo možné převést.")

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

# Zpracování dat pro roky 2023 a 2024
df_vykony_23, df_material_23 = load_and_prepare_data(23)
df_vykony_24, df_material_24 = load_and_prepare_data(24)

# Spojení všech dat
df_vykony_all = pd.concat([df_vykony_23, df_vykony_24], ignore_index=True)
df_material_all = pd.concat([df_material_23, df_material_24], ignore_index=True)


output_path = "data/processed/"
os.makedirs(output_path, exist_ok=True)

df_vykony_all.to_csv(os.path.join(output_path, "vykony_all.csv"), index=False, sep=";", encoding="utf-8")
df_material_all.to_csv(os.path.join(output_path, "material_all.csv"), index=False, sep=";", encoding="utf-8")

logging.info("Spojené tabulky uloženy:")
logging.info(f"- {output_path}vykony_all.csv")
logging.info(f"- {output_path}material_all.csv")
