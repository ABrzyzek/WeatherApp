import os.path
from typing import List

from fastapi import FastAPI
from fastapi.responses import FileResponse

from data.data_wunderground import get_station_names, read_data_from_csv
from data.schemas import Station, Weather

app = FastAPI()

@app.get('/')
def check_api():
    return {'Hello': 'World'}

@app.get('/stations', response_model=List[Station])
async def stations_list():
    return get_station_names()

@app.get('/weather/{filename}', response_model=List[Weather])
async def station(filename: str):
    return read_data_from_csv(f'{filename}.csv')

@app.get('/chart/{variable}')
async def chart(variable: str):
    if os.path.exists(f'data/files/{variable}_chart.png'):
        return FileResponse(f'data/files/{variable}_chart.png')
    else: return {'error': 'file_not_found'}