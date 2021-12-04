import pickle
import json
from typing import ValuesView
from pandas.core.dtypes.inference import is_number
from sleeper_wrapper import Players, League
from datetime import datetime


class sleeper_league:
    def __init__(self, update=True):
        if update:
            self.save_rosters()            
        else:
            with open('Dynasty_Sandwich/data/league_rosters_old.p', 'rb') as handle:
                self.rosters = pickle.load(handle)
            
    """Create the pickle-file 'league_rosters_old.p'.\n The file has informations about what players are in what roster."""
    def save_rosters(self):
        league = League(677930972028690432)
        roster_data = league.get_rosters()
        users = league.get_users()

        # roster_id:
        # - keys: user_id
        # - values: list of player_ids
        rosters_id = {} 
        for roster in roster_data:
            owner_id = roster.pop('owner_id')
            rosters_id[owner_id] = roster['players']

        data = {}
        rostered_players_id = []
        user_rosters_player_ids = {}
        rosters = {}
        for user in users: # iterate over list of league users
            user_name = user.pop('display_name').lower()        # get user_name
            user_id = user.pop('user_id')                           # get user_id
            rostered_players_id.extend(rosters_id[user_id])         # list of all rostered players
            user_rosters_player_ids[user_name] = rosters_id[user_id]     # dict with keys: user_name, values: list of player_ids
            rosters[user_name] = {'players': [], 'players_info': []} # create a dictionary for each user in the league (lists are filled in bellow)

        players = Players()
        all_players = players.get_all_players()

        for player_id in list(all_players.keys()):
            if player_id in rostered_players_id:
                for user_name in user_rosters_player_ids:
                    user_roster = user_rosters_player_ids[user_name]
                    if player_id in user_roster:
                        player_name = all_players[player_id]['full_name']
                        if type(player_name) == str:
                            player_name = player_name.replace("'","").replace('.','').lower()
                            rosters[user_name]['players'].append(player_name)
                            rosters[user_name]['players_info'].append((player_id, player_name))  
                        else:  
                            player_name = player_name[0].replace("'","").replace('.','').lower()
                            rosters[user_name]['players'].append(player_name)
                            rosters[user_name]['players_info'].append((player_id, player_name))

        with open('Dynasty_Sandwich/data/league_rosters_old.p', 'wb') as handle:
            pickle.dump(rosters, handle)
        self.rosters = rosters

    def Save_ID_USERS_dataset(self):
        """This function saves a dataset called users.txt which has information about what users have which id"""
        league = League(677930972028690432)
        roster_data = league.get_rosters()
        users = league.get_users()
        with open('Dynasty_Sandwich/data/ID_files/users_id.txt', 'w') as f:
            f.write('users,id')
            for user in users: # iterate over list of league users
                user_name = user['display_name'].lower()        # get user_name
                user_id = user['user_id']                          # get user_id
                f.write('\n{},{}'.format(user_name,user_id))


    """This function creates the datasets called QB.txt, ... WR.txt , which has information about what player has what ID"""
    def Save_ID_NAME_dataset(self):
        players = Players()
        all_players = players.get_all_players()

        WR = []
        RB = []
        TE = []
        QB = []
        for player_index in all_players:
            player_meta = all_players[player_index]
            if player_meta['position'] in ['WR', 'RB', 'QB', 'TE']:
                name = player_meta['full_name']
                id = player_meta['player_id']
                if player_meta['position'] == 'WR':
                    WR.append((name,id))
                elif player_meta['position'] == 'RB': 
                    RB.append((name,id))
                elif player_meta['position'] == 'TE':
                    TE.append((name,id))
                elif player_meta['position'] == 'QB':
                    QB.append((name,id))
                else:
                    cow = 'cow'
                    assert cow == 'horse'
        Positions = [('WR',WR), ('RB',RB), ('TE',TE), ('QB',QB)]
        for item in Positions:
            s = item[0]
            players = item[1]
            with open('Dynasty_Sandwich/data/ID_files/{}.txt'.format(s), 'w') as f:
                f.write('player,id')
                for player in players:
                    name = player[0].replace("'","").replace('.','').lower()
                    id = player[1]
                    f.write('\n{},{}'.format(name, id))


    """Get the value of each player as rated by keeptradecut"""
    def get_player_values(self):
        with open('Dynasty_Sandwich/data/keeptradecut.p', 'rb') as handle:
            df = pickle.load(handle)
        #print(df.head())
        player = 0

        for user_name in self.rosters:
            roster = self.rosters[user_name]['players']
            self.rosters[user_name]['values'] = []
            for player in roster:
                player_name = player.replace("'","").replace(".", "").lower()
                try:
                    val = df[df['Name'] == player_name]['Value']
                    self.rosters[user_name]['values'].append(int(val))
                except:
                    self.rosters[user_name]['values'].append(0)

        total_values = []
        for user_name in self.rosters:
            values = self.rosters[user_name]['values']
            players = self.rosters[user_name]['players']
            total_value = sum(values)
            total_values.append(total_value)
            self.rosters[user_name]['total_value'] = total_value
            
            values, players = zip(*sorted(zip(values, players), key=lambda t: t[0], reverse = True))
            self.rosters[user_name]['values'] = values
            self.rosters[user_name]['players'] = players

            print('\n-- {} ({}) -------------'.format(user_name, total_value))
            for i in range(len(values)):
                value = values[i]
                player_name = players[i]
                print('{}: \t {}'.format(value, player_name))

        with open('Dynasty_Sandwich/data/league_rosters.p', 'wb') as handle:
            pickle.dump(self.rosters, handle)

        order = ['vikkisibbi','ebb','thorsteinnah','agustlogi','thorsteinns','arnarleo','viktorhelgi','nonni123','tindurs','jonhugi97','birgirms','2g1c']
        with open('Dynasty_Sandwich/data/History.txt', 'a') as f:
            f.write('\n')
            time_now = datetime.now()
            date = '{}.{}.{}'.format(str(time_now.day), str(time_now.month), str(time_now.year))
            f.write(date)
            for user_name in order:
                total_value = self.rosters[user_name]['total_value']
                f.write('\t'+str(total_value))
                

    def analyze(self):
        for user_name in self.rosters:
            print('\n{}:'.format(user_name))
            for player in self.rosters[user_name]['players_info']:
                print('  - ', player)

    def create_data(self):
        for i in self.users:
            user_id = self.users['user_id']
            user_name = self.users['display_name']
            team = self.rosters['']


def sleeper_calculate(update = True):
    obj = sleeper_league(update=update)
    obj.get_player_values()

def update_player_ID_Dataset():
    obj = sleeper_league(update=True)
    obj.Save_ID_NAME_dataset()

def create_user_id_dataset():
    obj = sleeper_league(update=True)
    obj.Save_ID_USERS_dataset()

#create_user_id_dataset()

#update_player_ID_Dataset()

if __name__ == '__main__':
    sleeper_calculate()
    update_player_ID_Dataset()
    create_user_id_dataset()