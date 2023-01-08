import json
import pandas as pd
from datetime import datetime, timedelta, date
from typing import List
from urllib.request import urlopen

from data.schemas import Weather


def get_weather_for_station(station: str, start_date: datetime, end_date: datetime = date.today()) -> List[Weather]:
    list_weather = []
    while start_date.date() != end_date + timedelta(days=1):
        date = start_date.strftime('%Y%m%d')
        url = f'https://api.weather.com/v1/location/{station}:9:PL/observations/historical.json?apiKey=e1f10a1e78da46f5b10a1e78da96f525&units=e&startDate={date}'
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
            break
    return list_weather


def save_data_to_csv(weather_list: List[Weather]) -> None:
    data_set = pd.DataFrame([model.dict() for model in weather_list])
    start_date, end_date, city = weather_list[0].date.date(), weather_list[-1].date.date(), weather_list[0].city
    data_set.to_csv(rf'CSV\{city}_{start_date}_{end_date}.csv', index=False, sep=';')


save_data_to_csv(get_weather_for_station(station='EPWA', start_date=datetime(2023, 1, 5)))
