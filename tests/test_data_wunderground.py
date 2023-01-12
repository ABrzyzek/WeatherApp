from data.data_wunderground import *
from datetime import datetime
import pandas as pd
import os

def test_save_data_to_csv():
    #given
    weather_list = [Weather(date=datetime(2023,1,12), city="Warsaw", temperature=0, dev_point=1, humidity=2, wind="x", wind_speed=3, pressure=4, visibility=5, heat_index=6, weather_status="Fair"), Weather(date=datetime(2023,1,13), city="Warsaw", temperature=0, dev_point=11, humidity=21, wind="x", wind_speed=31, pressure=41, visibility=51, heat_index=61, weather_status="Fair")]
    #when
    save_data_to_csv(weather_list)
    #then
    data_set = pd.read_csv("files/Warsaw_2023-01-12_2023-01-13.csv", sep=";")
    data_set["date"] = pd.to_datetime(data_set["date"])
    data_set = data_set.replace(np.nan, None)
    expected_data = pd.DataFrame([model.dict() for model in weather_list])
    assert os.path.isfile("files\\Warsaw_2023-01-12_2023-01-13.csv")
    assert data_set.to_dict() == expected_data.to_dict()

def test_try_to_read_data_from_csv():
    try:
        read_data_from_csv("Warsaw_2023-01-01_2023-01-10.csv")
    except:
        assert False

def test_read_data_from_csv():
    #given
    city_name = "Warsaw"
    temperature = 57
    wind = "SW"
    wind_gust = None
    pressure = 29.57
    user_notes = None
    #when
    list_weather = read_data_from_csv("Warsaw_2023-01-01_2023-01-10.csv")
    #then
    assert city_name == list_weather[0].city
    assert temperature == list_weather[0].temperature
    assert wind == list_weather[0].wind
    assert wind_gust == list_weather[0].wind_gust
    assert pressure == list_weather[0].pressure
    assert user_notes == list_weather[0].user_notes

def test_try_to_get_data_frame_from_csv():
    try:
        get_data_frame_from_csv("Warsaw_2023-01-01_2023-01-10.csv")
    except:
        assert False

def test_get_data_frame_from_csv():
    #given
    date = "2023-01-01 00:00:00"
    wind_speed = 10
    precipitation = None
    weather_status = "Fair"
    #when
    data_frame_weather = get_data_frame_from_csv("Warsaw_2023-01-01_2023-01-10.csv")
    #then
    assert date == data_frame_weather["date"][0].strftime("%Y-%m-%d %H:%M:%S")
    assert weather_status == data_frame_weather["weather_status"][0]
    assert wind_speed == data_frame_weather["wind_speed"][0]
    assert precipitation == data_frame_weather["precipitation"][0]

def test_get_station_name():
    #given
    number_of_stations = 2
    first_station = Station(name = "Warsaw", code = "EPWA")
    second_station = Station(name = "Gdansk", code = "EPGD")
    #when
    list_stations = get_station_names()
    #then
    assert number_of_stations == len(list_stations)
    assert list_stations[0] == first_station
    assert list_stations[1] == second_station

def test_get_code_for_city():
    #given
    city_names = ["Warsaw","Gdansk"]
    proper_codes = ["EPWA","EPGD"]
    #when
    first_code = get_code_for_city(city_names[0])
    second_code = get_code_for_city(city_names[1])
    #then
    assert first_code == proper_codes[0] and second_code == proper_codes[1]