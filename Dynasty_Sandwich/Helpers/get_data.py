import pandas as pd
import numpy as np

def get_data(file_name, adjust_to_zero = False):
    worksheet = pd.read_excel(file_name, sheet_name = 'Sheet5')
    worksheet = worksheet[(worksheet.T != 0).any()]

    dates = worksheet.pop('Date')
    dates = np.array(dates)
    teams = worksheet.columns
    teams_values = np.array(worksheet)

    if adjust_to_zero:
        initial_values = teams_values[0,:]
        teams_values -= initial_values

    teams_values_temp = np.zeros(shape = teams_values.shape)
    teams_temp = []
    teams_rankings = teams_values[-1,:]
    teams_rankings = teams_rankings.argsort()[::-1]

    for i in range(teams_values.shape[1]):
        index = teams_rankings[i]
        teams_values_temp[:,i] = teams_values[:,index]
        teams_temp.append(teams[index])

    teams_values = teams_values_temp
    teams = teams_temp

    column_names = ['Dates']
    column_names.extend(teams)

    dates = dates.reshape([-1,1])

    data = np.concatenate([dates, teams_values], axis = 1)

    df = pd.DataFrame(data, columns=column_names)

    return df