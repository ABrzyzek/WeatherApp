from typing import Optional

from pydantic import BaseModel
from datetime import datetime


class Weather(BaseModel):
    date: datetime
    city: str
    temperature: int
    dev_point: int
    humidity: int
    wind: str
    wind_speed: int
    wind_gust: Optional[int]
    pressure: float
    precipitation: Optional[float]
    visibility: int
    heat_index: int
    weather_status: str
