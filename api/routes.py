import os.path
from datetime import date, datetime
from typing import List

from fastapi import FastAPI
from fastapi.responses import FileResponse

from data.data_wunderground import get_station_names, read_data_from_csv, get_weather_for_station, save_data_to_csv, \
    update_csv_for_new_data
from data.schemas import Station, Weather, Prediction, ChartType, Variables
from model.forecast import get_prediction_holt_winters, get_data_frame_for_variable, get_dashboard_for_data

FILE_NAME = 'test.csv'
app = FastAPI()


@app.get('/')
def check_api():
    return {200: 'success'}


@app.get('/stations', response_model=List[Station])
async def stations_list():
    return get_station_names()


@app.get('/weather', response_model=List[Weather])
async def weather():
    return read_data_from_csv(FILE_NAME)


@app.get('/chart/{variable}')
async def chart(variable: Variables, chart_type: ChartType):
    print(chart_type)
    if chart_type == ChartType.chart:
        get_dashboard_for_data(get_data_frame_for_variable(file_name=FILE_NAME, variable=variable), file_name=FILE_NAME)
    else:
        get_prediction_holt_winters(get_data_frame_for_variable(file_name=FILE_NAME, variable=variable), file_name=FILE_NAME)
    return FileResponse(f'data/files/{variable}{chart_type}')


@app.get('/prediction', response_model=Prediction)
async def prediction(variable: str):
    return get_prediction_holt_winters(get_data_frame_for_variable(file_name=FILE_NAME, variable=variable), file_name=FILE_NAME)


@app.get('/csvs')
async def csv_names():
    file_list, extension = os.listdir('data/files'), '.csv'
    return [string for string in file_list if string.endswith(extension)]


@app.get('/dashboards')
async def dashboards_names():
    file_list, extension = os.listdir('data/files'), '.png'
    return [string for string in file_list if string.endswith(extension)]


@app.put('/choose_csv')
async def change_csv(file_name: str):
    if os.path.exists(f'data/files/{file_name}'):
        global FILE_NAME
        FILE_NAME = file_name
        return {200: f'success, file name: {FILE_NAME}'}
    else:
        return {500: 'error'}


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
    if filename in os.listdir('data/files'):
        update_csv_for_new_data(filename)
        return {200: 'success'}
    return {500: 'error'}
