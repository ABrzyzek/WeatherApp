from typing import Union
import pandas as pd
from matplotlib import pyplot as plt
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.metrics import mean_absolute_error,mean_squared_error

from data.data_wunderground import get_data_frame_from_csv
from data.schemas import Error, Prediction, PredictionRow


def get_data_frame_for_variable(file_name: str, variable: str) -> Union[pd.DataFrame, None]:
    '''!
    Funkcja tworzy ramkę danych dla zmiennej oraz ustawia indeks jako datę
    '''
    data_set = get_data_frame_from_csv(file_name)
    column_names = data_set.columns.values.tolist()
    if variable in column_names:
        data_set = data_set[['date', variable]]
        data_set = data_set.set_index('date')
        return data_set
    return None


def get_dashboard_for_data(data: pd.DataFrame):
    '''!
    Funkcja pozwalająca na uzyskanie nazwy kolumny (nazwy zmiennej) oraz generująca wykres uzyskanej zmiennej
    '''
    name = data.columns.values.tolist()[-1]
    data[[name]].plot(title=f'{name} dashboard',figsize = (12,8))
    plt.savefig(f"data/files/{name}_chart.png", bbox_inches='tight')


def get_prediction_holt_winters(data: pd.DataFrame) -> Prediction:
    '''!
    Funkcja tworząca model predykcji Holta Wintera dla 6 kolejnych okresów (3 godz.).
    Generuje wykres predykcji oraz wykres zależności testu i predykcji.
    Liczy średni błąd kwadratowy oraz średni błąd bezwzględny.
    '''
    name = data.columns.values.tolist()[-1]
    x = data[name]
    n = 6
    a = int(len(x))
    train_weather = x[:a - n]
    test_weather = x[a - n:]
    fitted_model = ExponentialSmoothing(train_weather, trend='mul').fit()
    test_predictions = fitted_model.forecast(steps=n)
    train_weather.plot(legend=True, label='TRAIN')
    test_weather.plot(legend=True, label='TEST', figsize=(6, 4))
    test_predictions.plot(legend=True,label='PREDICTION')
    plt.savefig(f"data/files/{name}_prediction_chart.png", bbox_inches='tight')
    plt.clf()
    test_weather.plot(legend=True, label='TEST', figsize=(9, 6))
    test_predictions.plot(legend=True, label='PREDICTION')
    plt.title('Train, Test and Predicted Test using Holt Winters')
    plt.savefig(f"data/files/{name}_prediction_test_chart.png", bbox_inches='tight')
    error = Error(mean_absolute_error=mean_absolute_error(test_weather, test_predictions),
                  mean_squared_error=mean_squared_error(test_weather, test_predictions))
    list_prediction = []
    for date, value in test_predictions.items():
        row = PredictionRow(date=date.to_pydatetime(), value=value)
        list_prediction.append(row)
    return Prediction(name=name, error=error, prediction=list_prediction)