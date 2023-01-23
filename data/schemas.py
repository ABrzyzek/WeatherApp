from enum import Enum
from typing import Optional, List

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
    user_notes: Optional[str]


class Station(BaseModel):
    name: str
    code: str


class ChartType(str, Enum):
    chart = '_chart.png'
    chart_prediction = '_prediction_chart.png'
    chart_test_prediction = '_prediction_test_chart.png'


class Chart(BaseModel):
    name: ChartType


class PredictionRow(BaseModel):
    date: datetime
    value: float


class Error(BaseModel):
    mean_absolute_error: float
    mean_squared_error: float


class Prediction(BaseModel):
    name: str
    prediction: List[PredictionRow]
    error: Error

