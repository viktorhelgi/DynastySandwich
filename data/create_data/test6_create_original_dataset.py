from numpy.core.getlimits import _register_known_types
import pandas as pd
import pickle
from DataObjects.League import Players
 


class PlayerNotFoundError(Exception):
    """Player was not found in the dataset"""
    pass

def get_player_info(player_name) -> Players:
    dataset = 'data/nfl_players.p'

    with open(dataset, 'rb') as handle:
        data = pickle.load(handle)
        df:pd.DataFrame = data['df']
        df = df.fillna('unknown')
        if player_name == 'irv smith jr':
            player_name = 'irv smith'
        row = df[df['merge_name'] == player_name]
        if len(row) >= 2:
            row = row[row['position'].isin(['QB', 'RB', 'WR', 'TE'])]
        if len(row) >= 2:
            print()
            print(row.head(len(row)))
            selected_row = int(input('\n select row: '))
        else: 
            selected_row = 0
    if len(row) == 0:
        return {}
    else:
        return row.iloc[selected_row,:]
    
    
def get_KTC_collection() -> Players:
    players = Players()
    # Get player_names
    with open('C:/Users/Lenovo/Documents/VSCode_Tests/NFL/Dynasty_Sandwich/data/keeptradecut_collection.p', 'rb') as handle:
        df_players = pickle.load(handle)
        df_players.pop('Date')
        np_players = df_players.to_numpy()
    players_names = list(df_players.columns)

    # iterate over all players
    for i, player_name in enumerate(players_names):
        if player_name[0:4].isdigit():
            continue
        current_value = np_players[-1,i]
        history_value = np_players[:,i]
        other_data = get_player_info(player_name=player_name)
        if len(other_data) != 0:
            players.add_player(
                name            = player_name,
                value           = current_value, 
                value_history   = history_value.tolist(),
                position    = other_data['position'],
                sleeper_id  = other_data['sleeper_id'],
                ktc_id      = other_data['ktc_id'],
                birthdate   = other_data['birthdate'],
                team        = other_data['team'],
                draft_pick  = other_data['draft_pick'],
                draft_round = other_data['draft_round'],
                draft_ovr  = other_data['draft_ovr'],
                weight      = other_data['weight'],
                height      = other_data['height']
            )            
    return players


players:Players = get_KTC_collection()




players.save_obj()