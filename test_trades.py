from sleeper_wrapper import Players, League
from Dynasty_Sandwich.Helpers.sleeper_id import sleeper_helper
from HelperFunctions.bcolors import bcol

import matplotlib
import numpy as np
import pandas as pd
from datetime import datetime
import copy
import sys
from collections import OrderedDict
"""
> league_trans = league.get_transactions(week)
> transaction_1 = league_trans[0]
> transaction_1.keys()
    dict_keys([
        'waiver_budget', 
        'type', 
        'transaction_id', 
        'status_updated', 
        'status', 
        'settings', 
        'roster_ids', 
        'metadata', 
        'leg', 
        'drops', 
        'draft_picks', 
        'creator', 
        'created', 
        'consenter_ids', 
        'adds'
    ])
"""

class Trade_Compiler:
    def __init__(self, transaction_type = None, weeks = False, manager = None, print_type = 0, operation = 'get_info'):
        print("__init__")
        self.print_type = print_type
        self.manager = manager
        if type(manager) == str:
            self.adds = []
            self.drops = []
            print('Function not Implemented for "type(manager) == str:"')
            if operation == 'get_info':
                self.get_info(
                    manager = manager,
                    transaction_type = transaction_type
                )
                self.print_summary()
            elif operation == 'get':
                self.get(
                    manager = manager,
                    transaction_type = transaction_type
                )
                self.print_summary()
        elif type(weeks) == list or type(weeks).__module__ == 'numpy':
            self.get_info(
                weeks = np.array(weeks)
            )
        else: 
            self.get_info()

    def get_info(self, weeks = None, manager = 'all', transaction_type = 'trade'):
        print('get_info')
        weeks = np.arange(0,7,1)
        print('')
        league = League(677930972028690432)



        sleeper = sleeper_helper()
        dct = OrderedDict()
        df  = pd.DataFrame(columns = ['user', 'add/drop', 'player', 'date', 'transaction_id', 'transaction_type', 'trader'])
        df['transaction_id'] = pd.to_numeric(df['transaction_id'])
        for id, user in sleeper.user_sub_ids.items(): 
            dct[id] = {'manager': user, 'weeks': {}, 'drops': [], 'adds': []}
            for week in weeks: dct[id]['weeks'][week] = {'trades': [], 'drops': [], 'adds': []}
        
        transaction_id = 0
        for week in weeks:
            league_trans = league.get_transactions(week)
            print(bcol.B.n + '\n Week ', week, '' + bcol.reset)
            managers_in_trades = {}
            managers_in_F_or_W = {}
            i = 0
            for transaction in league_trans:
                if len(df) != 0:
                    transaction_id = df['transaction_id'].max()+1

                # what should we check for 
                
                type_is_F_or_W     = transaction['type'] == 'waiver' or transaction['type'] == 'free_agent'
                type_is_trade      = transaction['type'] == 'trade'
                managers_in_trade = []
                # If view trades
                if type_is_trade:
                    
                    print(bcol.B.dgr + '\n- TRADE' + bcol.reset)
                    managers_in_trade.extend(list(transaction['adds'].values())) if transaction['adds'] != None else None
                    managers_in_trade.extend(list(transaction['drops'].values())) if transaction['drops'] != None else None
                    
                    # If draft picks included in trade
                    if len(transaction['draft_picks']) != 0:
                        for pick in transaction['draft_picks']:
                            managers_in_trade.extend([pick['owner_id'], pick['previous_owner_id']]) 

                    managers_in_trade = list(np.unique(managers_in_trade).astype('int'))

                    for user_id in managers_in_trade:
                        user = sleeper.user_sub_ids[user_id]
                        dct[user_id]['weeks'][week]['trades'].append({'adds': [], 'drops': []})

                    if transaction['adds'] != None:
                        for player_id, user_id in transaction['adds'].items():
                            date  = datetime.utcfromtimestamp(transaction['status_updated']/1000).date()
                            new_owner = dct[user_id]['manager']
                            player    = sleeper.get_player_name(player_id)
                            trader    = sleeper.user_sub_ids[transaction['drops'][player_id]]

                            dct[user_id]['adds'].append(player_id)
                            dct[user_id]['weeks'][week]['adds'].append([player_id, 'trade'])
                            dct[user_id]['weeks'][week]['trades'][len(dct[user_id]['weeks'][week]['trades'])-1]['trader'] = trader
                            dct[user_id]['weeks'][week]['trades'][len(dct[user_id]['weeks'][week]['trades'])-1]['adds'].append(player)
                            df_row  = pd.DataFrame(
                                [[new_owner, 'add', player, date, transaction_id, 'trade', trader]],
                                columns = ['user', 'add/drop', 'player', 'date', 'transaction_id', 'transaction_type', 'trader']
                            )
                            df = df.append(df_row, ignore_index=True)

                    if transaction['drops'] != None:
                        for player_id, user_id in transaction['drops'].items():
                            date  = datetime.utcfromtimestamp(transaction['status_updated']/1000).date()
                            pre_owner = dct[user_id]['manager']
                            player    = sleeper.get_player_name(player_id)
                            trader    = sleeper.user_sub_ids[transaction['adds'][player_id]]

                            dct[user_id]['drops'].append(player_id)
                            dct[user_id]['weeks'][week]['drops'].append([player_id, 'drops'])
                            dct[user_id]['weeks'][week]['trades'][len(dct[user_id]['weeks'][week]['trades'])-1]['trader'] = trader
                            dct[user_id]['weeks'][week]['trades'][len(dct[user_id]['weeks'][week]['trades'])-1]['drops'].append(player)
                            df_row  = pd.DataFrame(
                                [[pre_owner, 'drop', player, date, transaction_id, 'trade', trader]],
                                columns = ['user', 'add/drop', 'player', 'date', 'transaction_id', 'transaction_type', 'trader']
                            )
                            df = df.append(df_row, ignore_index=True)
                    if len(transaction['draft_picks']) != 0:
                        for pick in transaction['draft_picks']:
                            date  = datetime.utcfromtimestamp(transaction['status_updated']/1000).date()
                            new_owner_id = pick['owner_id']
                            pre_owner_id = pick['previous_owner_id']
                            new_owner    = sleeper.user_sub_ids[new_owner_id]
                            pre_owner    = sleeper.user_sub_ids[pre_owner_id]

                            pick_round = pick['round']
                            pick_year  =  pick['season']
                            pick_origin = sleeper.user_sub_ids[pick['roster_id']]
                            pick_info = '{} - {} round via {}'.format(pick_year, pick_round, pick_origin)
                            
                            dct[new_owner_id]['adds'].append(pick_info)
                            dct[pre_owner_id]['drops'].append(pick_info)

                            dct[new_owner_id]['weeks'][week]['trades'][len(dct[new_owner_id]['weeks'][week]['trades'])-1]['adds'].append(pick_info)
                            dct[pre_owner_id]['weeks'][week]['trades'][len(dct[pre_owner_id]['weeks'][week]['trades'])-1]['drops'].append(pick_info)
                            df_row  = pd.DataFrame(
                                [[new_owner, 'add', pick_info, date, transaction_id, 'trade', trader]],
                                columns = ['user', 'add/drop', 'player', 'date', 'transaction_id', 'transaction_type', 'trader']
                            )
                            df = df.append(df_row, ignore_index=True)
                            df_row  = pd.DataFrame(
                                [[pre_owner, 'drop', pick_info, date, transaction_id, 'trade', trader]],
                                columns = ['user', 'add/drop', 'player', 'date', 'transaction_id', 'transaction_type', 'trader']
                            )
                            df = df.append(df_row, ignore_index=True)

                    #print('')
                    #print(dct[managers_in_trade[0]]['manager'])
                    #print(dct[managers_in_trade[0]]['weeks'][week]['trades'])
                    #print('')
                    #print(dct[managers_in_trade[1]]['manager'])
                    #print(dct[managers_in_trade[1]]['weeks'][week]['trades'])
                    #print('')

                elif type_is_F_or_W:
                    date  = datetime.utcfromtimestamp(transaction['status_updated']/1000).date()
                    manager = sleeper.user_sub_ids[transaction['roster_ids'][0]]
                    if transaction['adds'] != None:
                        for player_id, user_id in transaction['adds'].items():
                            player    = sleeper.get_player_name(player_id)
                            df_row  = pd.DataFrame(
                                [[manager, 'add', player, date, transaction_id, transaction['type'], 'None']],
                                columns = ['user', 'add/drop', 'player', 'date', 'transaction_id', 'transaction_type', 'trader']
                            )
                            df = df.append(df_row, ignore_index=True)
                    if transaction['drops'] != None:
                        for player_id, user_id in transaction['drops'].items():
                            player    = sleeper.get_player_name(player_id)
                            df_row  = pd.DataFrame(
                                [[manager, 'drop', player, date, transaction_id, transaction['type'], 'None']],
                                columns = ['user', 'add/drop', 'player', 'date', 'transaction_id', 'transaction_type', 'trader']
                            )
                            df = df.append(df_row, ignore_index=True)
                else:
                    print(bcol.I.y + ' - ' + transaction['type'] + bcol.reset)            
                i += 1


        df.to_csv('Dynasty_Sandwich/data/Transactions.csv')
            
        ## If view Waiver of Free Agent Pickup
        #if type_is_F_or_W:
        #    print(transaction)
        #    print('\n')
        #    user_id = transaction['roster_ids'][0]
        #    user = sleeper.user_sub_ids[user_id]
        #    if user not in managers_in_F_or_W.keys():
        #        managers_in_F_or_W[user] = [int(i)]
        #    else:
        #        managers_in_F_or_W[user].append(int(i))
        #    
        #
        #
        #
                ##else:
                ##    print(transaction['type'])    
                
            #league_trans_trades = np.array([])
            #league_trans_F_or_W = np.array([])
            #if manager in managers_in_trades.keys():
            #    league_trans_trades = np.array(league_trans)[np.array(managers_in_trades[manager]).astype(int)]
            #    print(league_trans_trades.shape)
            #if manager in managers_in_F_or_W.keys():
            #    league_trans_F_or_W = np.array(league_trans)[np.array(managers_in_F_or_W[manager]).astype(int)]
            #    print(league_trans_F_or_W.shape)
            #    
            #league_trans
        
    def get(self, weeks = np.arange(0,18,1), manager = 'all', transaction_type = 'trade'):
        print('get')
        league = League(677930972028690432)

        for week in weeks:
            league_trans = league.get_transactions(week)
            sleeper = sleeper_helper()
            k = 0
            if manager != 'all':
                managers_in_trades = {}
                managers_in_F_or_W = {}
                i = 0
                for transaction in league_trans:
                    # what should we check for 
                    print_all_trans  = transaction_type == 'all'

                    type_is_F_or_W     = transaction['type'] == 'waiver' or transaction['type'] == 'free_agent'
                    type_is_trade      = transaction['type'] == 'trade'

                    print_only_trade   = transaction_type == 'trade'
                    print_only_F_or_W  = transaction_type == 'waiver' or transaction_type == 'free_agent'

                    managers_in_trade = []
                    if (print_all_trans and type_is_trade) or (print_only_trade and type_is_trade):
                        managers_in_trade.extend(list(transaction['adds'].values())) if transaction['adds'] != None else None
                        managers_in_trade.extend(list(transaction['drops'].values())) if transaction['drops'] != None else None
                        if len(transaction['draft_picks']) != 0:
                            for pick in transaction['draft_picks']:
                                managers_in_trade.extend([pick['owner_id'], pick['previous_owner_id']]) 
                        managers_in_trade = list(np.unique(managers_in_trade).astype('int'))
                        for user_id in managers_in_trade:
                            user = sleeper.user_sub_ids[user_id]
                            if user not in managers_in_trades.keys():
                                managers_in_trades[user] = [int(i)]
                            else:
                                managers_in_trades[user].append(int(i))

                    if (print_all_trans and type_is_F_or_W) or (print_only_F_or_W and type_is_F_or_W):
                        print(transaction)
                        print('\n')
                        user_id = transaction['roster_ids'][0]
                        user = sleeper.user_sub_ids[user_id]
                        if user not in managers_in_F_or_W.keys():
                            managers_in_F_or_W[user] = [int(i)]
                        else:
                            managers_in_F_or_W[user].append(int(i))
                        



                    #else:
                    #    print(transaction['type'])    
                    i += 1
                league_trans_trades = np.array([])
                league_trans_F_or_W = np.array([])
                if manager in managers_in_trades.keys():
                    league_trans_trades = np.array(league_trans)[np.array(managers_in_trades[manager]).astype(int)]
                    print(league_trans_trades.shape)
                if manager in managers_in_F_or_W.keys():
                    league_trans_F_or_W = np.array(league_trans)[np.array(managers_in_F_or_W[manager]).astype(int)]
                    print(league_trans_F_or_W.shape)
                    
                league_trans



            if manager == 'all' or manager in managers_in_trades.keys():
                if len(league_trans) != 0:
                    print(
                        bcol.BU.dgr + '_'*50,
                        "\n\nWEEK " + str(week) + bcol.reset, '\n'
                    ) if self.print_type == 0 else None
                for transaction in league_trans:
                    k += 1
                    t_type = transaction['type']
                    t_id   = transaction['transaction_id']
                    t_userid = transaction['creator']
                    t_users = transaction['roster_ids']
                    t_user   = sleeper.get_user_name(int(t_userid))
                    if t_type == 'trade':
                        user1 = sleeper.user_sub_ids[transaction['roster_ids'][0]]
                        user2 = sleeper.user_sub_ids[transaction['roster_ids'][1]]
                        date  = datetime.utcfromtimestamp(transaction['status_updated']/1000).date()
                        print(bcol.B.dgr + 'TRADE: {} - {} ({})'.format(user1, user2, date) + bcol.reset)   if self.print_type == 0 else None
                        if transaction['adds'] != None:
                            for player_id in transaction['adds']:
                                user_id = transaction['adds'][player_id]
                                user = sleeper.user_sub_ids[user_id]
                                print(bcol.B.b + '{}: {}{}'.format(user, ' '*(19-len(user)), sleeper.get_player_name(player_id)) + bcol.reset)  if self.print_type == 0 else None
                                if manager != 'all' and manager == user:
                                    self.adds.append(sleeper.get_player_name(player_id))
                        if len(transaction['draft_picks']) != 0:
                            for pick in transaction['draft_picks']:
                                user_id = pick['owner_id']
                                user    = sleeper.user_sub_ids[user_id]
                                pick_round = pick['round']
                                pick_year  =  pick['season']
                                pick_origin = sleeper.user_sub_ids[pick['roster_id']]
                                pick_info = '{} - {} round via {}'.format(pick_year, pick_round, pick_origin)
                                print(bcol.B.b + '{}: {}{}'.format(user, ' '*(19-len(user)), pick_info) + bcol.reset)   if self.print_type == 0 else None
                                if manager != 'all' and manager == user:
                                    self.adds.append(pick_info)
                            #for jj in range(len(transaction['draft_picks'])):   
                            #    print(transaction['draft_picks'][jj])
                        if transaction['drops'] != None:
                            for player_id in transaction['drops']:
                                user_id = transaction['drops'][player_id]
                                user = sleeper.user_sub_ids[user_id]
                                print(bcol.B.r + '{}:{}{}'.format(user, ' '*(20-len(user)), sleeper.get_player_name(player_id)) +  bcol.reset)  if self.print_type == 0 else None
                                if manager != 'all' and manager == user:
                                    self.drops.append(sleeper.get_player_name(player_id))
                        if len(transaction['draft_picks']) != 0:
                            for pick in transaction['draft_picks']:
                                user_id = pick['previous_owner_id']
                                user    = sleeper.user_sub_ids[user_id]
                                pick_round = pick['round']
                                pick_year  =  pick['season']
                                pick_origin = sleeper.user_sub_ids[pick['roster_id']]
                                pick_info = '{} - {} round via {}'.format(pick_year, pick_round, pick_origin)
                                print(bcol.B.r  + '{}: {}{}'.format(user, ' '*(19-len(user)), pick_info) + bcol.reset)  if self.print_type == 0 else None
                                if manager != 'all' and manager == user:
                                    self.drops.append(pick_info)
                        print('')   if self.print_type == 0 else None
                    else:
                        print(t_type)

    def print_summary(self):
        print(
            bcol.B.n + 
            '\n---------------------------------------------------------' + 
            '\n                  Summary - {}'.format(self.manager) + 
            '\n---------------------------------------------------------\n'
        )
        
        adds_temp = copy.deepcopy(self.adds)
        drops_temp = copy.deepcopy(self.drops)
        for i, item in enumerate(adds_temp):
            if item in drops_temp:
                self.adds.remove(item)
                self.drops.remove(item)

        self.adds.sort()
        self.drops.sort()
        n = max(len(self.adds), len(self.drops))
        print(bcol.BU.dgr + "Adds" + bcol.reset + " "*(35-len("Adds")) + bcol.BU.dgr + "Dropps" + bcol.reset)
        for i in range(n):
            if i < len(self.adds) and i < len(self.drops):
                print(bcol.B.b + self.adds[i] + " "*(35-len(self.adds[i])) + bcol.B.r + self.drops[i])
            elif i < len(self.adds):
                print(bcol.B.b + self.adds[i])
            elif i < len(self.drops):
                print(" "*(35) + bcol.B.r + self.drops[i])
        print('' + bcol.reset)
weeks = np.arange(0,2,1)



obj = Trade_Compiler(manager = 'viktorhelgi', transaction_type = 'trade', print_type = 0, operation = 'get')

"""
self.user_sub_ids = {
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
"""
        