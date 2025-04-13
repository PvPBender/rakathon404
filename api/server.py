from fastapi import FastAPI, Request
from pydantic import BaseModel

from parsers import ambulanceMessage, releaseMessage, patParser, rtgParser, vykParser, bioParser, hemParser

app = FastAPI()

def createServer():
    pass

@app.get("/api")
def index():
    return {"status": "true"}


@app.post("/api/createModel/{pacientID}")
async def create_model(pacientID: str):
    json_path = Path("frontend/static/patient_98332.json")
    with open(json_path, "r", encoding="utf-8") as f:
        json_data = json.load(f)

    return json_data

@app.post("/api/parse/ambulanceMessage")
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

@app.post("/api/parse/releaseMessage")
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


@app.post("/api/parse/patMessage")
async def parse_pat_message(req: Request):


    data = await req.body()
    message = data.decode("windows-1250")


    parsed = patParser.parseFile(message)
    if parsed is None:
        return {"status": "false"}

    # todo return filled template

@app.post("/api/parse/lab/{type}")
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


@app.post("/api/parse/rtg")
async def parse_lab_message(req: Request):


    data = await req.body()
    message = data.decode("windows-1250")

    parsed = rtgParser.parseFile(message)
    if parsed is None:
        return {"status": "false"}
    
    # todo return filled template



# ===================== FRONTEND
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import json

TEAM = [
    "Bára Kindlová",
    "Dalibor Trampota",
    "Honza",
    "Daniij"
]

# Mount static files (CSS, images, etc.)
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# Jinja2 templates folder
templates = Jinja2Templates(directory="frontend/templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):

    json_name_path = Path("model/patient-template.json")    
    with open(json_name_path, "r", encoding="utf-8") as f:
        name_data = json.load(f)
        
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "name": "404 Cancer Not Found",
        "name_data": name_data,
        "team": TEAM,
    })

