import nfl_data_py as nfl
import pandas as pd
import pickle

df = nfl.import_ids(
    columns = [
        'name', 'merge_name', 
        'position', 'team', 
        'birthdate', 'height', 'weight',
        'draft_round', 'draft_pick', 'draft_ovr'
    ],
    ids = ['ktc', 'sleeper']
)

info = '\n'.join([
    '| The data is a pandas dataframe from nfl_data_py.',
    '| >> data = nfl.import_ids(columns = cols, ids = ids)',
    "| columns: \n| - 'name', 'merge_name', \n| - 'position', 'team', \n| - 'birthdate', 'height', 'weight', \n| - 'draft_round', 'draft_pick', 'draft_ovr'",
    "| ids: 'ktc', 'sleeper "
])

Data = {'info':info, 'df':df}

with open('C:/Users/Lenovo/Documents/VSCode_Tests/NFL/data/nfl_players.p', 'wb') as handle:
    pickle.dump(Data, handle)

