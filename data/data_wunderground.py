import json
import yaml

import numpy as np
import pandas as pd
from datetime import datetime, timedelta, date
from typing import List, Union
from urllib.request import urlopen

from data.schemas import Weather, Station


def get_weather_for_station(station_code: str, start_date: datetime, end_date: datetime = date.today()) -> List[
    Weather]:
    list_weather = []
    while start_date != end_date + timedelta(days=1):
        date = start_date.strftime('%Y%m%d')
        url = f'https://api.weather.com/v1/location/{station_code}:9:PL/observations/historical.json?apiKey=e1f10a1e78da46f5b10a1e78da96f525&units=e&startDate={date}'
        response = urlopen(url)
        data_json = json.loads(response.read())['observations']
        for data in data_json:
            weather = Weather(date=start_date, city=data['obs_name'], temperature=data['temp'],
                              dev_point=data['dewPt'], humidity=data['rh'], wind=data['wdir_cardinal'],
                              wind_speed=data['wspd'], wind_gust=data['gust'], pressure=data['pressure'],
                              precipitation=data['precip_hrly'], visibility=data['vis'], heat_index=data['heat_index'],
                              weather_status=data['wx_phrase'])
            list_weather.append(weather)
            start_date += timedelta(minutes=30)
        if start_date.hour != 0 or start_date.minute != 0:
            return list_weather
    return list_weather


def save_data_to_csv(weather_list: List[Weather]) -> None:
    data_set = pd.DataFrame([model.dict() for model in weather_list])
    start_date, end_date, city = weather_list[0].date.date(), weather_list[-1].date.date(), weather_list[0].city
    data_set.to_csv(rf'files\{city}_{start_date}_{end_date}.csv', index=False, sep=';')


def read_data_from_csv(filename: str) -> List[Weather]:
    data_set = pd.read_csv(rf'files/{filename}', sep=';')
    data_set = data_set.replace(np.nan, None)
    list_weather = []
    for row in data_set.T.to_dict().values():
        list_weather.append(Weather(**row))
    return list_weather


def get_data_frame_from_csv(filename: str) -> pd.DataFrame:
    return pd.DataFrame([model.dict() for model in read_data_from_csv(filename)])


def get_station_names() -> List[Station]:
    list_stations = []
    with open(r'files\stations.yaml') as file:
        stations = yaml.full_load(file)
        for name, code in stations.items():
            list_stations.append(Station(name=name, code=code))
    return list_stations


def get_code_for_city(city_name: str) -> str:
    stations = get_station_names()
    for station in stations:
        if city_name == station.name:
            return station.code
    return ''


def update_csv_for_new_data(filename: str):
    list_weather = read_data_from_csv(filename)
    last_date = list_weather[-1].date.date()
    last_date = datetime(last_date.year, last_date.month, last_date.day)
    station_code = get_code_for_city(list_weather[0].city)
    new_list_weather = get_weather_for_station(start_date=last_date, station_code=station_code)
    list_weather = [weather for weather in list_weather if weather not in new_list_weather]
    list_weather += new_list_weather
    save_data_to_csv(list_weather)
