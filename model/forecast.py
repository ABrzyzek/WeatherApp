import pandas as pd
from matplotlib import pyplot as plt

from data.data_wunderground import get_data_frame_from_csv

def get_data_frame_for_variable(file_name: str, variable: str) -> pd.DataFrame:
    data_set = get_data_frame_from_csv(file_name)
    column_names = data_set.columns.values.tolist()
    return data_set[['date', variable]] if variable in column_names else None


def get_dashboard_for_data(data: pd.DataFrame):
    data = data.set_index('date')
    name = data.columns.values.tolist()[-1]
    data[[name]].plot(title=f'{name} dashboard',figsize = (12,8))
    plt.show()

