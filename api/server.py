from fastapi import FastAPI, Request
from pydantic import BaseModel

from parsers import ambulanceMessage, releaseMessage, patParser, rtgParser, vykParser, bioParser, hemParser

app = FastAPI()

def createServer():
    pass

@app.get("/")
def index():
    return {"status": "true"}


@app.post("/parse/ambulanceMessage")
async def parse_ambulance_message(req: Request):
    """
    Parses the ambulance message and returns the parsed data
    """
    
    data = await req.body()
    message = data.decode("windows-1250")

    parsed = ambulanceMessage.parseReport(message)
    if parsed is None:
        return {"status": "false"}
    
    # todo return filled template

@app.post("/parse/releaseMessage")
async def parse_release_message(req: Request):
    """
    Parses the ambulance message and returns the parsed data
    """
    
    data = await req.body()
    message = data.decode("windows-1250")

    parsed = releaseMessage.parseReport(message)
    if parsed is None:
        return {"status": "false"}
    
    # todo return filled template


@app.post("/parse/patMessage")
async def parse_pat_message(req: Request):


    data = await req.body()
    message = data.decode("windows-1250")


    parsed = patParser.parseFile(message)
    if parsed is None:
        return {"status": "false"}

    # todo return filled template

@app.post("/parse/lab/{type}")
async def parse_lab_message(labType: str, req: Request):


    data = await req.body()
    message = data.decode("windows-1250")

    parsed = None
    if labType == "bio":
        parsed = bioParser.parseFile(message)
    elif labType == "hem":
        parsed = hemParser.parseFile(message)
    else:
        return {"message": "Unknown lab type. Valid types are: bio, hem"}

    if parsed is None:
        return {"status": "false"}


    # todo return filled template


@app.post("/parse/rtg")
async def parse_lab_message(req: Request):


    data = await req.body()
    message = data.decode("windows-1250")

    parsed = rtgParser.parseFile(message)
    if parsed is None:
        return {"status": "false"}
    
    # todo return filled template


