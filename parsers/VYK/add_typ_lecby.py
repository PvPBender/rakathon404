import logging
import os
import pandas as pd


def annotate_vykony_with_names(vykony_csv, kod_ciselnik, output_csv):
    """
    Merge a list of výkon KODs with a name dictionary and export the result.

    Args:
        vykony_csv (str): Path to CSV file with performance data (must contain column 'KOD')
        kod_ciselnik (str): Path to CSV with mapping of KOD -> NAZEV_VYKONU
        output_csv (str): Output CSV path
    """
    logging.info("Loading data...")
    df_vykony = pd.read_csv(vykony_csv, sep=";", encoding="utf-8")
    df_kody = pd.read_csv(kod_ciselnik, sep=",", encoding="utf-8")

    # Prepare for merge
    df_kody = df_kody.rename(columns={"code": "KOD", "name": "NAZEV_VYKONU"})
    df_kody["KOD"] = df_kody["KOD"].astype(str).str.strip()
    df_vykony["KOD"] = df_vykony["KOD"].astype(str).str.strip()

    # Merge
    df_annotated = df_vykony.merge(df_kody, on="KOD", how="left")

    # Reorder columns
    cols = list(df_annotated.columns)
    if "KOD" in cols and "NAZEV_VYKONU" in cols:
        cols.remove("NAZEV_VYKONU")
        insert_idx = cols.index("KOD") + 1
        cols.insert(insert_idx, "NAZEV_VYKONU")
        df_annotated = df_annotated[cols]

    # Stats
    annotated_count = df_annotated["NAZEV_VYKONU"].notna().sum()
    total_count = len(df_annotated)
    logging.info(f"Annotated records: {annotated_count} out of {total_count}")

    # Save
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    df_annotated.to_csv(output_csv, sep=";", encoding="utf-8", index=False)
    logging.info(f"Saved to: {output_csv}")
