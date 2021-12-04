import requests
import sys
import json
import pickle
import numpy as np
import pandas as pd
from datetime import datetime
import copy

class keeptrade_cut:
    def __init__(self):
        self.url = 'https://keeptradecut.com/dynasty-rankings?page=0&filters=QB|WR|RB|TE|RDP&format=1'
    def scraper(self, save_original = False):
        obj = requests.get(self.url)
        data = obj.content
        str_data = data.decode()
        players_data = str_data.split('var playersArray = [{')[1]
        k = 0
        for i in range(len(players_data)):
            if players_data[i] == '\n':
                k = i-1
                break
        string_data = players_data[:k]
        strings_data = []
        ss = 0
        for i in range(len(string_data)):
            if "playerName" in string_data[i:i+10]:
                strings_data.append(string_data[ss:i])
                ss = i
        strings_data.append(string_data[ss:len(string_data)-2])

        str_data = ''.join(strings_data)
        str_data = str_data.replace('},{"playerName', '},SPLIT{"playerName')
        info = str_data.split('},SPLIT{')
        self.data = {}

        for i in range(len(info)):
            player_dict = json.loads('{'+info[i]+'}')
            player_name = player_dict.pop('playerName')
            self.data[player_name] = player_dict

        if save_original:
            with open('players_data2.p', 'wb') as handle:
                pickle.dump(self.data, handle)



    def analyze_pickle(self):
        with open('players_data2.p', 'rb') as handle:
            data = pickle.load(handle)
            
        for key1 in data['Christian Kirk'].keys():
            val1 = data['Christian Kirk'][key1]
            print('\n- {}:'.format(key1))
            if type(val1) == dict:
                for key2 in val1.keys():
                    print('  - {}:'.format(key2))
                    val2 = val1[key2]
                    if type(val2) == dict:
                        for key3 in val2.keys():
                            val3 = val2[key3]
                            print('    - {}:'.format(key3))
                            print('      > {}'.format(repr(val3)))
                    else:
                        print('    > {}'.format(repr(val2)))
            else:
                print('  > {}'.format(repr(val1)))

    def create_dataframe(self):
        players = self.data
        player_names = []
        players_info = []
        #datetime.datetime(1996, 6, 7, 5, 0)
        today = datetime.now()
        for name in players.keys():
            player_data = players[name]
            if '20' == name[:2]:
                Rank = player_data['oneQBValues']['rank']
                Value = player_data['oneQBValues']['value']
                players_info.append([name, np.nan, Rank, Value, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan])
            else:
                player_name = name.replace("'", "").replace(".", "").lower()
                ID_nr = player_data['playerID']
                Rank = player_data['oneQBValues']['rank']
                Value = player_data['oneQBValues']['value']
                Position = player_data['position']
                Team = player_data['teamLongName']
                Team_El = player_data['team']
                Number = player_data['number']
                Rookie = player_data['rookie']
                Age = (today - datetime.utcfromtimestamp(int(player_data['birthday']))).days/365.25 
                Height = player_data['heightFeet']*0.3048 + player_data['heightInches']*0.0254
                Weight = player_data['weight']*0.4535924
                Exp = player_data['seasonsExperience']
                Pick = 32*(player_data['pickRound']-1) + player_data['pickNum']
                players_info.append([player_name, ID_nr, Rank, Value, Position, Team, Team_El, Number, Rookie, Age, Height, Weight, Exp, Pick])
               
        stats = ['Name','ID', 'Rank', 'Value', 'Position', 'Team', 'Team_El', 'Nr', 'IsRookie', 'Age', 'Height', 'Weight', 'SeasonsExp', 'Pick']
        df = pd.DataFrame(players_info, columns = stats)

        with open('Dynasty_Sandwich/data/keeptradecut.p', 'wb') as handle:
            pickle.dump(df, handle)
            
        with open('Dynasty_Sandwich/data/keeptradecut_collection.p', 'rb') as handle:
            data = pickle.load(handle)

        n = list(df['Name'].to_numpy())
        names = ['Date']
        names.extend(n)

        v = list(df['Value'].to_numpy())
        vals = [datetime.now()]
        vals.extend(v)

        new_data = pd.DataFrame([vals], columns = names)

        for col in data.columns:
            if col not in new_data.columns:
                new_col2 = pd.DataFrame([[0]], columns = [col])
                new_data = pd.concat([new_data, new_col2], axis = 1)
        
        for col in new_data.columns:
            if col not in data.columns:
                new_col = np.zeros(shape = (len(data),1))
                y = pd.DataFrame(new_col, columns= [col])
                data = pd.concat([data,y], axis = 1)

        data = pd.concat([data,new_data], ignore_index=True)

        with open('Dynasty_Sandwich/data/keeptradecut_collection.p', 'wb') as handle:
            pickle.dump(data, handle)
        
    def create_save_dataframe(self):
        with open('Dynasty_Sandwich/data/keeptradecut.p', 'rb') as handle:
            data = pickle.load(handle)
        Player_Names = list(data['Name'].to_numpy())
        Player_Values = [list(data['Value'].to_numpy())]

        df = pd.DataFrame(Player_Values, columns = Player_Names)

        with open('Dynasty_Sandwich/data/keeptradecut_collection.p', 'wb') as handle:
            pickle.dump(df, handle)

    def check_dataframe(self):
        with open('Dynasty_Sandwich/data/keeptradecut_collection.p', 'rb') as handle:
            data = pickle.load(handle)

        new_data = copy.deepcopy(data)
        new_data.pop('kyle allen')

        new_col = pd.DataFrame([[1]], columns = ['add'])
        new_data = pd.concat([new_data,new_col], axis = 1)
        data = pd.concat([data,data], ignore_index=True)
        
        for col in data.columns:
            if col not in new_data.columns:
                new_col2 = pd.DataFrame([[0]], columns = [col])
                new_data = pd.concat([new_data, new_col2], axis = 1)
        
        for col in new_data.columns:
            if col not in data.columns:
                new_col = np.zeros(shape = (len(data),1))
                y = pd.DataFrame(new_col, columns= [col])
                data = pd.concat([data,y], axis = 1)

        data = pd.concat([data,new_data], ignore_index=True)


def update_keeptradecut():
    obj = keeptrade_cut()
    obj.scraper()
    obj.create_dataframe()
