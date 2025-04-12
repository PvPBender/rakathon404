import os
from utils import readFile, parseHeader
from User import User
import re
import regex as rx

BASE_PATH = os.getcwd() + "/data/DATA/PAC/PROPOUŠTĚCÍ ZPRÁVA"

def parseReport(msg: str) -> User | None:
    """
    Parses a single report and returns a dictionary of the data
    """
    u = None
    try:
        [info, _, reason, *lines] = msg.splitlines()

        u = parseHeader(info)
        u.set("acceptReason", reason)


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




def parseFile(file: str) -> list[User]:
    """
    Parses a single file of reports
    """
    [_, *msgs] = re.split(r"^===\s", file, flags=re.MULTILINE)
    users: list[User] = []
    for report in msgs:
        if user := parseReport(report):
            users.append(user)
        
    return users


def parse():
    users: list[User] = []
    for year in [2023, 2024]:
        dir = BASE_PATH + f"/{year}/"
        for file in os.listdir(dir):
            print("Parsing", file)
            data = readFile(dir + file)
            parsed = parseFile(data)
            users.extend(parsed)

    return users




if __name__ == "__main__":
    parsedUsers = parse()
    
    print(parsedUsers[0], len(parsedUsers))

