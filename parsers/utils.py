import re
from parsers.User import User
from pathlib import Path
import pandas as pd

def readFile(path):
    """
    Reads a file and returns its contents as a string.
    """
    with open(path, "r", encoding="windows-1250") as f:
        return f.read()

def parseHeader(header: str) -> User | None:
    infoRes = re.search(r"\d+\. (?P<id>\d+) / (?P<y>\d{2})(?P<g>\d)X+ / \d+", header)
    if infoRes == None:
        print("No patient ID found!", infoRes, header)
        return None
    
    u = User()
    u.set("id", infoRes.group(1)) # group 0 is the whole string
    u.set("year", infoRes.group(2))
    u.setGender(infoRes.group(3))

    u.set("temp", header)

    return u

def projectRoot() -> Path:
    current_dir = Path(__file__).resolve()
    project_root = current_dir.parents[1]
    return project_root

def pathTo(*paths) -> Path:
    """
    Joins the given paths to the project root directory.
    """
    return projectRoot().joinpath(*paths)

    
def clean_datetime_columns(df: pd.DataFrame, datetime_columns: list) -> pd.DataFrame:
    """
    Cleans datetime columns by ensuring the correct datetime format for MySQL.
    """
    for col in datetime_columns:
        if col in df.columns:
            # Convert to datetime and format as 'YYYY-MM-DD HH:MM:SS'
            df[col] = pd.to_datetime(df[col], errors='coerce').dt.strftime('%Y-%m-%d %H:%M:%S')
    return df
