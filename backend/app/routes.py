import os
from typing import Dict, Optional
from fastapi import APIRouter, HTTPException, Query
import httpx

from app.models import MetOfficeRawResponse, MetOfficeTimeSeriesItem, WeatherResponse
from app.constants import MET_OFFICE_CODES

router = APIRouter()

WEATHER_API_KEY: Optional[str] = os.getenv("WEATHER_API_KEY")

@router.get("/weather", response_model=WeatherResponse)
async def get_weather(
    lat: float = Query(51.5074, description="Latitude"),
    lon: float = Query(-0.1278, description="Longitude")
  ) -> WeatherResponse:
    if not WEATHER_API_KEY:
      raise HTTPException(status_code=500, detail="API key is missing on the server.")

    url: str = "https://data.hub.api.metoffice.gov.uk/sitespecific/v0/point/hourly"
    headers: Dict[str, str] = {"apikey": WEATHER_API_KEY, "accept": "application/json"}
    params: Dict[str, float] = {"latitude": lat, "longitude": lon}

    async with httpx.AsyncClient() as client:
       try:
          response = await client.get(url, headers=headers, params=params, timeout=5.0)
          response.raise_for_status()
       except httpx.HTTPStatusError as exc:
          raise HTTPException(status_code=exc.response.status_code, detail="Met Office API error")
       except httpx.RequestError:
          raise HTTPException(status_code=503, detail="Weather service unavailable")

    try:
       parsed_data: MetOfficeRawResponse = MetOfficeRawResponse.model_validate(response.json())
       current: MetOfficeTimeSeriesItem = parsed_data.features[0].properties.timeSeries[0]
       code: Optional[int] = current.screenWeatherCode

       return WeatherResponse(
          temperature=round(current.screenTemperature),
          feels_like=round(current.feelsLikeTemperature),
          humidity=round(current.screenRelativeHumidity),
          wind_speed=round(current.windSpeed10m),
          condition=MET_OFFICE_CODES.get(code if code is not None else -1, "Cloudy"),
          timestamp=current.time
       )
    except Exception:
       raise HTTPException(status_code=500, detail="Error parsing Met Office response format")