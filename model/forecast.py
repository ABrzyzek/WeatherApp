from typing import Union

import pandas as pd
from matplotlib import pyplot as plt

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
    pass
