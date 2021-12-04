import nfl_data_py as nfl
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#import seaborn as sns

def get_player_positions(pos = ['QB', 'RB', 'WR', 'TE']):
    wd = nfl.import_weekly_data(years = [2020])
    print(wd.to_numpy().shape)

    ids = nfl.import_ids()
    

    data = nfl.import_rosters(years = [2020])
    ids_pos_names = data[['player_name', 'player_id', 'position']]
    ids_pos_names

    out = pd.merge(wd, ids_pos_names, on =  'player_id' )

    print(out.to_numpy().shape)
    out = out[out['position'].isin(pos)]
    return out

def get_player_info():
    pass

#data = get_player_positions(pos = ['WR'])
#print(data.columns)
#
#sns.histplot(data = data, x = 'week', y = 'fantasy_points')
#plt.show()