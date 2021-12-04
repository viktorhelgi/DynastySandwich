from DataObjects.League import Player, Players, Team, League, WhoIsthisHesNotaManagerError
from DataObjects.Player_IDs_Sleeper import get_sleeper_ids, PlayersIDs

from Dynasty_Sandwich.Helpers.sleeper_id import sleeper_helper

from typing import Optional, List
import pickle
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider


from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar



import numpy as np
import datetime
from HelperFunctions.code_guide import PointToFunction

import time

def create_player_dataset(players_ids:PlayersIDs) -> Players:
    """Get Players from keeptradecut_collection.p and create a Players object."""
    # Create an the Players object:
    players = Players()
    # Get player_names
    with open('C:/Users/Lenovo/Documents/VSCode_Tests/NFL/Dynasty_Sandwich/data/keeptradecut_collection.p', 'rb') as handle:
        df_players = pickle.load(handle)
        df_players.pop('Date')
        np_players = df_players.to_numpy()
    players_names = list(df_players.columns)

    # iterate over all players
    for i, player_name in enumerate(players_names):
        current_value = np_players[-1,i]
        history_value = np_players[:,i]
        players.add_player(
            name = player_name,
            value = current_value, 
            value_history = history_value.tolist()
        )
    return players


def get_league(KTC_players:Players) -> League:
    with open('C:/Users/Lenovo/Documents/VSCode_Tests/NFL/Dynasty_Sandwich/data/league_rosters.p', 'rb') as handle:
        roster_data = pickle.load(handle)
    rosters = []
    for manager in roster_data:
        players = Players()
        for _, name in roster_data[manager]['players_info']:   
            if name in KTC_players.names:
                value = int(KTC_players[name].value)
                value_history = KTC_players[name].value_history
            else:
                #print(name)
                # player not in KTC_players dataset
                value = 0

            players.add_player(
                name = name,
                value = value, 
                value_history = value_history
            )
            
        players = players.create_new_object(sort_attr='value')
        rosters.append(Team(manager, players))
    return League(rosters)

def test(league:League) -> None:
    managers = league
    manager = league['viktorhelgi']
    player  = manager['jamarr chase']
    print(
        f'\n\nmanagers\n\n{managers}',
        f'\n\nmanager\n\n{manager}',
        f'\n\nplayer\n\n{player}'
    )


def plot_manager_status(league:League, manager:str) -> None:
    roster = league[manager].players  # Players

    fig = plt.figure(figsize=(15,8))
    ax = fig.subplots(1,1)
    box = ax.get_position()                
    ax.set_position([box.x0, box.y0, box.width * 0.7, box.height])

    y_max = (max(roster.values)//1000)*1000+1
    print(y_max)
    ax.set_yticks(np.arange(0, y_max+1000, step=500))
    ax.grid()

    initial_loc = 1
    ax.set_ylim([y_max*initial_loc - 1000,y_max*initial_loc +  1000])

    plt.gca().set_prop_cycle(plt.cycler('color', plt.cm.turbo(np.linspace(0, 1, 12))))

    n_dim = len(league['viktorhelgi']['jamarr chase'].value_history)
    today = datetime.datetime.now()
    today = datetime.datetime(today.year, today.month, today.day)
    xaxis = [today- datetime.timedelta(days=i) for i in range(n_dim)][::-1]

    n_players = len(league[manager].players.players)
    colors = list(plt.cm.turbo(np.linspace(0, 1, int(np.ceil(n_players/3)*3))[np.random.permutation(n_players)].tolist()))
    style  = ['-', '--', '-.', ':']*int(np.ceil(n_players/4))

    cc = zip(roster.players, list(plt.cycler(color=colors)),list(plt.cycler(linestyle=style)))
    for player, color, style  in cc:
        ax.plot(xaxis, player.value_history, label = player.name, color=color['color'], linestyle=style['linestyle'])
        ax.annotate(player.name, (xaxis[-1], player.value_history[-1]), fontsize=6)
    handles, labels = ax.get_legend_handles_labels()


    def event_mouse_scroll(event:mpl.backend_bases.MouseEvent) -> None:
        if event.button == 'up':
            change=+100
        elif event.button == 'down':
            change=-100
        lims = event.canvas.figure.axes
        ymin, ymax = lims[0].get_ylim()
        lims[0].set_ylim(ymin+change, ymax+change)
        fig.canvas.draw()
    fig.canvas.mpl_connect('scroll_event', event_mouse_scroll)

    #scroller = Slider(axlim, 'ylim', 0, 1.0, valinit=initial_loc, orientation='vertical', initcolor=None)
    # ymin -> 1000*initial_loc - 1500 =  8500
    # ymax -> 1000*initial_loc +  500 = 10500
    #def event_drag_scroll_bar(val):
    #    ax.set_ylim([y_max*val - 1500 , y_max*val + 500])
    #    fig.canvas.draw_idle()
    #scroller.on_changed(event_drag_scroll_bar)

    ax.set_title(manager)
    plt.legend( handles, labels, loc='center left', bbox_to_anchor=(1.2, 0.5))
    plt.show()

@PointToFunction()
def main_plot_test(manager):
    c = time.perf_counter_ns()
    players_sleeper_ids:PlayersIDs = get_sleeper_ids()
    KTC_players = create_player_dataset(players_sleeper_ids)
    my_league  = get_league(KTC_players=KTC_players)
    
    #test(league=my_league)    
    #print(sleeper_helper.user_sub_ids.values())

    if manager not in sleeper_helper.user_sub_ids.values():
        ErrorMsg = f"\n\nThis guy [{manager}] is not a manager.\n Select one of the following \n -  ebb  \n -  thorsteinns  \n -  nonni123  \n -  agustlogi  \n -  arnarleo  \n -  birgirms   \n -  viktorhelgi  \n -  2g1c  \n -  tindurs  \n -  vikkisibbi  \n -  thorsteinnah  \n -  jonhugi97 "
        raise WhoIsthisHesNotaManagerError(ErrorMsg)
    
    plot_manager_status(league=my_league, manager=manager)


if __name__ == '__main__':    
    main_plot_test()
    

#
#    ms = 0
#    for i in (300):
#        c = time.perf_counter_ns()
#        players_sleeper_ids:PlayersIDs = get_sleeper_ids()
#        KTC_players = create_player_dataset(players_sleeper_ids)
#        my_league  = get_league(all_players=KTC_players)
#        test(league=my_league)
# 
#        ns = time.perf_counter_ns()-c
#        ms += ns/(10**6)
#        print(f'i: \t {ms} milli seconds')
# without slots : 18739.987899999986
# with slots :    17422.261400000003
# without slots : 17925.642799999983
# with slots:     15602.748199999993

#def fn():
#    with open('C:/Users/Lenovo/Documents/VSCode_Tests/NFL/Dynasty_Sandwich/data/keeptradecut_collection.p', 'rb') as handle:
#        players = pickle.load(handle)
#
#    with open('C:/Users/Lenovo/Documents/VSCode_Tests/NFL/Dynasty_Sandwich/data/league_rosters.p', 'rb') as handle:
#        rosters = pickle.load(handle)
#
#    for i in rosters:
#        print(i)

