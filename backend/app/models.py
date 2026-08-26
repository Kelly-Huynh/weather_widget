from typing import List, Optional
from pydantic import BaseModel, Field

class MetOfficeTimeSeriesItem(BaseModel):
  time: str
  screenTemperature: float
  feelsLikeTemperature: float
  screenRelativeHumidity: float
  windSpeed10m: float
  screenWeatherCode: Optional[int] = None

class MetOfficeProperties(BaseModel):
  timeSeries: List[MetOfficeTimeSeriesItem]

class MetOfficeFeature(BaseModel):
  properties: MetOfficeProperties

class MetOfficeRawResponse(BaseModel):
  features: List[MetOfficeFeature]

class WeatherResponse(BaseModel):
  temperature: int = Field(..., description="Temperature in Celsius")
  feels_like: int = Field(..., description="Feels-like temperature in Celsius")
  humidity: int = Field(..., description="Relative humidity percentage")
  wind_speed: int = Field(..., description="Wind speed in mph")
  condition: str = Field(..., description="Human-readable weather status")
  timestamp: str = Field(..., description="ISO timestamp of weather observation")