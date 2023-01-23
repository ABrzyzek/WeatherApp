from typing import Union
import pandas as pd
from matplotlib import pyplot as plt
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.metrics import mean_absolute_error,mean_squared_error

from data.data_wunderground import get_data_frame_from_csv


def get_data_frame_for_variable(file_name: str, variable: str) -> Union[pd.DataFrame, None]:
    data_set = get_data_frame_from_csv(file_name)
    column_names = data_set.columns.values.tolist()
    if variable in column_names:
        data_set = data_set[['date', variable]]
        data_set = data_set.set_index('date')
        return data_set
    return None


def get_dashboard_for_data(data: pd.DataFrame):
    name = data.columns.values.tolist()[-1]
    data[[name]].plot(title=f'{name} dashboard',figsize = (12,8))
    plt.savefig(f"data/files/{name}_chart.png", bbox_inches='tight')


def get_prediction_holt_winters(data: pd.DataFrame):
    name = data.columns.values.tolist()[-1]
    print(data[name])

    weather = pd.read_csv('weather.csv', sep=',', index_col='date', parse_dates=True)
    x = weather['temperature']

    n = 6
    a = int(len(x))
    train_weather = x[:a - n]
    test_weather = x[a - n:]
    print(test_weather)

    fitted_model = ExponentialSmoothing(train_weather, trend='mul').fit()
    test_predictions = fitted_model.forecast(steps=n)

    x.plot(legend=True, title='temperature')
    train_weather.plot(legend=True, label='TRAIN')
    test_weather.plot(legend=True, label='TEST', figsize=(6, 4))
    test_predictions.plot(legend=True,label='PREDICTION')

    test_weather.plot(legend=True, label='TEST', figsize=(9, 6))
    test_predictions.plot(legend=True, label='PREDICTION')

    plt.title('Train, Test and Predicted Test using Holt Winters')
    plt.show()

    error = [mean_absolute_error(test_weather, test_predictions), mean_squared_error(test_weather, test_predictions)]
    return test_predictions, error