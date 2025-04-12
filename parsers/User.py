

class User:
    def __init__(self):
        self.temp = None
        self.file = None

        self.id = None
        self.doctor = ""
        self.year = None
        self.gender = None
        self.body = None
        self.acceptReason = None
        self.titles = []

    def __str__(self):
        return f"User(id={self.id}, doctor={self.doctor}, year={self.year}, sex={self.gender} body=...)"

    def set(self, name, value):
        setattr(self, name, value)

    def setGender(self, value):
        if value == 1 or value == 2:
            self.gender = 0
        elif value == 5 or value == 6:
            self.gender = 1

    def getBody(self):
        return self.body

    