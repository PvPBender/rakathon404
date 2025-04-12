import logging
import os
import pandas as pd


def annotate_vykony_with_names(vykony_csv_or_df, kod_ciselnik,
                               output_csv=None):
    """
    Merge a list of výkon KODs with a name dictionary and optionally export the result.

    Args:
        vykony_csv_or_df (str or pd.DataFrame): Path to CSV soubor nebo již načtený DataFrame
        kod_ciselnik (str): Path to CSV with mapping of KOD -> NAZEV_VYKONU
        output_csv (str or None): Optional path to output CSV

    Returns:
        pd.DataFrame: Annotated výkon DataFrame
    """
    logging.info("Loading data...")

    # Vstup: cesta nebo DataFrame
    if isinstance(vykony_csv_or_df, str):
        df_vykony = pd.read_csv(vykony_csv_or_df, sep=";", encoding="utf-8")
    elif isinstance(vykony_csv_or_df, pd.DataFrame):
        df_vykony = vykony_csv_or_df.copy()
    else:
        raise ValueError(
            "vykony_csv_or_df musí být buď string (path), nebo pandas DataFrame.")

    df_kody = pd.read_csv(kod_ciselnik, sep=",", encoding="utf-8")
    df_kody = df_kody.rename(columns={"code": "KOD", "name": "NAZEV_VYKONU"})
    df_kody["KOD"] = df_kody["KOD"].astype(str).str.strip()
    df_vykony["KOD"] = df_vykony["KOD"].astype(str).str.strip()

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

    if output_csv is not None:
        output_dir = os.path.dirname(output_csv)
        if output_dir:  # vytvoř adresář jen pokud cesta není prázdná
            os.makedirs(output_dir, exist_ok=True)
        df_annotated.to_csv(output_csv, sep=";", encoding="utf-8", index=False)
        logging.info(f"Saved to: {output_csv}")

    return df_annotated
