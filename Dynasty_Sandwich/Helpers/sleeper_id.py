import pandas as pd



class sleeper_helper:
    user_sub_ids = {
             1: 'ebb',
             2: 'thorsteinns',
             3: 'nonni123',
             4: 'agustlogi',
             5: 'arnarleo',
             6: 'birgirms', 
             7: 'viktorhelgi',
             8: '2g1c',
             9: 'tindurs',
             10: 'vikkisibbi',
             11: 'thorsteinnah',
             12: 'jonhugi97'
        }
    def __init__(self):
        self.All_players = None
        self.data_QB = pd.read_csv('Dynasty_Sandwich/data/ID_files/QB.txt', sep=",",  encoding = "ISO-8859-1")
        self.data_WR = pd.read_csv('Dynasty_Sandwich/data/ID_files/WR.txt', sep=",",  encoding = "ISO-8859-1")
        self.data_RB = pd.read_csv('Dynasty_Sandwich/data/ID_files/RB.txt', sep=",",  encoding = "ISO-8859-1")
        self.data_TE = pd.read_csv('Dynasty_Sandwich/data/ID_files/TE.txt', sep=",",  encoding = "ISO-8859-1")
        self.data = pd.concat([self.data_QB, self.data_WR, self.data_RB, self.data_TE])

        self.data_Users = pd.read_csv('Dynasty_Sandwich/data/ID_files/users_id.txt', sep=",",  encoding = "ISO-8859-1")
        self.users_ids = self.data_Users['users'].to_numpy()


    def get_player_name(self, id, pos = None):
        if pos == None:
            return self.data[self.data['id'] == int(id)].player.values[0]
        elif pos == 'WR':
            return self.data_WR[self.data_WR['id'] == int(id)].player.values[0]
        elif pos == 'RB':
            return self.data_RB[self.data_RB['id'] == int(id)].player.values[0]
        elif pos == 'TE':
            return self.data_TE[self.data_TE['id'] == int(id)].player.values[0]
        elif pos == 'QB':
            return self.data_QB[self.data_QB['id'] == int(id)].player.values[0]
    def get_user_name(self, id):
        if id < 20:
            return self.users_ids[id]
        else:
            return self.data_Users[self.data_Users['id'] == int(id)].users.values[0]


