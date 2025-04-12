import os
from parsers.utils import readFile, parseHeader
from parsers.User import User
import re
import regex as rx

BASE_PATH = os.getcwd() + "/data/DATA/PAC/AMBULATNÍ ZPRÁVA"

MAX_DOC_LENGTH = 100 # max(enumerate([len(u.doctor) for u in parsedUsers]), key=lambda x: x[1])[0]

def parseReport(msg: str) -> User | None:
    """
    Parses a single report and returns a dictionary of the data
    """
    u = None
    try:
        lines = msg.splitlines()
        if len(lines) == 1:
            print("Empty entry for:", msg.strip())
            return None
        
        if len(lines) < 3:
            u = parseHeader(lines[0])
            if len(lines[1]) < MAX_DOC_LENGTH:
                u.set("doctor", lines[1])
            else:
                u.set("body", lines[1])    
            return u
        
        [info, doc, *lines] = lines
        u = parseHeader(info)
        if len(doc) < MAX_DOC_LENGTH:
            u.set("doctor", doc)
        else:
            lines.insert(0, doc)

        body = "\n".join(lines)
        u.set("body", body)

        titles = rx.findall(r"^(\p{L}+):", body, flags=re.MULTILINE)
        if titles != []:
            u.set("titles", titles)
            
    except Exception as err:
        print("Error parsing report\n", err)
        print(msg)
        return None
        
    return u




def parseFile(file: str, fileName: str | None) -> list[User]:
    """
    Parses a single file of reports and returns a list of parsed data
    """
    [_, *msgs] = re.split(r"^===\s", file, flags=re.MULTILINE)
    users: list[User] = []
    for report in msgs:
        if user := parseReport(report):
            if fileName:
                user.set("file", fileName)
            users.append(user)
        
    return users


def parse():
    """
    Parses all files that are for this parser and returns a list of parsed data
    It should use parseFile to parse each file to avoid code duplication
    """
    users: list[User] = []
    for year in [2023, 2024]:
        dir = BASE_PATH + f"/{year}/"
        for file in os.listdir(dir):
            print("Parsing", file)
            data = readFile(dir + file)
            parsed = parseFile(data, file)
            users.extend(parsed)

    return users




if __name__ == "__main__":
    parsedUsers = parse()
    print(parsedUsers[0], len(parsedUsers))

