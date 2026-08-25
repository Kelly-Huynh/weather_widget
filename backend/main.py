from fastapi import FastAPI
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

import requests
import os

load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

app = FastAPI()

@app.get('/weather')
async def get_weather(lat: float, lon: float) -> JSONResponse:
    url = "https://data.hub.api.metoffice.gov.uk/sitespecific/v0/point/hourly"
    headers = {
        "apikey": WEATHER_API_KEY,
        "accept": "application/json"
    }
    params = {
        "latitude": lat,
        "longitude": lon
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json()