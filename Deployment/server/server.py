from fastapi import FastAPI,Response,Request,Form,HTTPException
import json
import util as util
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import logging

app = FastAPI()


templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})




@app.get("/get_location_names")
def get_location_names():
    response={
        "locations":util.get_location_name()
    }

    return response


@app.post("/predict_home_prices")
async def predict_home_price(request:Request,area:int = Form(...),location:str = Form(...),bath:int = Form(...),bhk:int = Form(...)):
    try:
        sqftVal = area
        bathVal = bath
        bhkVal = bhk
        locationVal = location

        est_price = util.get_estimated_price(locationVal,bhkVal,bathVal,sqftVal)

        # print(est_price)
        response={
            'estimated_price':est_price
        }
        return response
    except Exception as e:
        return {"error":f"error has been occured {e}"}
    