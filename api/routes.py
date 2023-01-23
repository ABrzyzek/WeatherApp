import os.path
from datetime import date, datetime
from typing import List

from fastapi import FastAPI
from fastapi.responses import FileResponse

from data.data_wunderground import get_station_names, read_data_from_csv, get_weather_for_station, save_data_to_csv, update_csv_for_new_data
from data.schemas import Station, Weather

app = FastAPI()


@app.get('/')
def check_api():
    return {200: 'success'}


@app.get('/stations', response_model=List[Station])
async def stations_list():
    return get_station_names()


@app.get('/weather/{filename}', response_model=List[Weather])
async def station(filename: str):
    return read_data_from_csv(f'{filename}.csv')


@app.get('/chart/{variable}')
async def chart(variable: str, chart_type: str):
    if os.path.exists(f'data/files/{variable}_chart.png'):
        return FileResponse(f'data/files/{variable}_chart.png')
    else:
        return {500: 'error'}


@app.get('/prediction')
async def prediction(variable: str):
    pass


@app.get('/csvs')
async def csv_names():
    file_list, extension = os.listdir('data/files'), '.csv'
    return [string for string in file_list if string.endswith(extension)]


@app.post('/choose_csv')
async def change_csv():
    pass


@app.post('/create_csv')
async def create_csv(station_name: str, start_date: date, end_date: date = date.today()):
    stations = get_station_names()
    for station in stations:
        if station.name == station_name:
            save_data_to_csv(
                get_weather_for_station(
                    station_code=station.code,
                    start_date=datetime(start_date.year, start_date.month, start_date.day),
                    end_date=datetime(end_date.year, end_date.month, end_date.day)))
    if os.path.exists(f'data/files/{station_name}_{start_date}_{end_date}.csv'):
        return {200: 'successful'}
    return {500: 'error'}


@app.post('/update_csv')
async def create_csv(filename: str):
    if f'{filename}.csv' in os.listdir('data/files'):
        update_csv_for_new_data(filename)
        return {200: 'success'}
    return {500: 'error'}
