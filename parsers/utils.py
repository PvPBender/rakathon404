import re
from parsers.User import User

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