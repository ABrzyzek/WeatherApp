from model.forecast import *
from data.data_wunderground import get_data_frame_from_csv
import pandas as pd
import os

def test_get_data_frame_for_variable():
    #given
    file_name = "test.csv"
    variable = "temperature"
    expected_number_of_variables = 336
    expected_head_output = pd.DataFrame({"temperature": [57, 57, 57, 57, 57]}, index=pd.to_datetime(["2023-01-01 00:00:00", "2023-01-01 00:30:00", "2023-01-01 01:00:00", "2023-01-01 01:30:00", "2023-01-01 02:00:00"]))
    expected_tail_output = pd.DataFrame({"temperature": [41, 39, 41, 41, 41]}, index=pd.to_datetime(["2023-01-07 21:30:00", "2023-01-07 22:00:00", "2023-01-07 22:30:00", "2023-01-07 23:00:00", "2023-01-07 23:30:00"]))
    #when
    output = get_data_frame_for_variable(file_name, variable)
    head_output = output.head()
    tail_output = output.tail()
    #then
    assert head_output.equals(expected_head_output)
    assert tail_output.equals(expected_tail_output)
    assert expected_number_of_variables == len(output)

def test_get_data_frame_for_variable_invalid_input():
    #given
    file_name = "test.csv"
    variable = "invalid"
    #when
    output = get_data_frame_for_variable(file_name, variable)
    #then
    assert output is None

def test_get_dashboard_for_data():
    #given
    data = pd.DataFrame({"temperature": [41, 39, 41, 38, 40]}, index=pd.to_datetime(["2023-01-07 21:30:00", "2023-01-07 22:00:00", "2023-01-07 22:30:00", "2023-01-07 23:00:00", "2023-01-07 23:30:00"]))
    #when
    get_dashboard_for_data(data)
    #then
    assert os.path.exists(f"data/files/temperature_chart.png")
    os.remove(f"data/files/temperature_chart.png")