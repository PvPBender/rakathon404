import os


BASE_PATH = os.getcwd() + "/data/DATA/PAC"


def parseFile(file: str) -> list[any]:
    """
    Parses a single file of reports and returns a list of parsed data
    """
    [_, *msgs] = re.split(r"^===\s", file, flags=re.MULTILINE)
    users: list[any] = []
    for report in msgs:
        if user := parseReport(report):
            users.append(user)
            
    return users

def parse() -> list[any]:
    """
    Parses all files that are for this parser and returns a list of parsed data
    It should use parseFile to parse each file to avoid code duplication
    """
    pass
    



if __name__ == "__main__":
    parse()