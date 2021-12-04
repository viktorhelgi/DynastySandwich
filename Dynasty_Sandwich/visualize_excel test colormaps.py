# Local Modules
import HelperFunctions.terminal_traceback
from Dynasty_Sandwich.Helpers.get_file_name import get_file_name
from Dynasty_Sandwich.Helpers.get_data import get_data
from Dynasty_Sandwich.Helpers.get_date import get_date
# Packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import math

class league:
    def __init__(self, colormap):
        self.file_name = get_file_name()

        data_values = get_data(self.file_name)
        self.dates = np.array(data_values.pop('Dates'))
        self.names = data_values.columns
        self.teams_values = np.array(data_values)

        data_change = get_data(self.file_name, adjust_to_zero = True)
        data_change.pop('Dates')
        self.names_changes = data_change.columns
        self.teams_changes = np.array(data_change)

        self.colormap = colormap

    def get_xticks(self):
        x_ticks = []
        dattt = []
        if 30*3 <= len(self.dates):
            for i, date in enumerate(list(self.dates)):
                date_info = date.split('.')
                if len(date_info) == 3:
                    day = date_info[0]
                    year = date_info[2]
                    if (day == '1' or day == '15') and len(year) == 4:
                        x_ticks.append(i)
                        dattt.append(date)
        else:
            for i, date in enumerate(list(self.dates)):
                date_info = date.split('.')
                if len(date_info) == 3:
                    day = date_info[0]
                    year = date_info[2]
                    if ((int(day))%2 == 0) and len(year) == 4:
                        x_ticks.append(i)
                        dattt.append(date)
        plt.xticks(x_ticks)
        
    def plot_teams(self, teams_values, dates, teams):
        fig = plt.figure(figsize=(8,8))
        ax = plt.subplot(111)

        if self.colormap == 0:
            plt.gca().set_prop_cycle(plt.cycler('color', plt.cm.gist_earth(np.linspace(0, 1, 12))))
        elif self.colormap == 1:
            plt.gca().set_prop_cycle(plt.cycler('color', plt.cm.ocean(np.linspace(0, 1, 12))))
        elif self.colormap == 2:
            plt.gca().set_prop_cycle(plt.cycler('color', plt.cm.gnuplot(np.linspace(0, 1, 12))))
        elif self.colormap == 3:
            plt.gca().set_prop_cycle(plt.cycler('color', plt.cm.brg(np.linspace(0, 1, 12))))
        elif self.colormap == 4:
            plt.gca().set_prop_cycle(plt.cycler('color', plt.cm.rainbow(np.linspace(0, 1, 12))))
        elif self.colormap == 5:
            plt.gca().set_prop_cycle(plt.cycler('color', plt.cm.turbo(np.linspace(0, 1, 12))))
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 1.2, box.height])

        if teams_values.shape[1] == 12:
            plot_order = [0,11,5,8,2,9,6,1,7,3,4,10]
            for i in plot_order:
                plt.plot(dates, teams_values[:,i],  label = teams[i])
            handles, labels = ax.get_legend_handles_labels()
            order = teams_values[-1,[0,11,5,8,3,9,6,1,7,2,4,10]]
            order, labels, handles = zip(*sorted(zip(order, labels, handles), key=lambda t: t[0]))
            plt.legend( handles[::-1], labels[::-1], loc='center left', bbox_to_anchor=(1, 0.5))
        else:
            for i in range(teams_values.shape[1]):
                plt.plot(dates, teams_values[:,i],  label = teams[i])
            plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        fig.autofmt_xdate()

        plt.subplots_adjust(left=0.1, right=0.79, top=0.75, bottom=0.1)
    
    def change_time_period(self, start_date=None, end_date=None, teams_values=None, dates=None, return_output = False):
        if type(teams_values).__module__!='numpy' or type(dates).__module__!='numpy':
            teams_values = self.teams_values
            dates = self.dates
        start_date = get_date(start_date, 'start')
        end_date = get_date(end_date, 'end')

        index_1 = 100000
        index_2 = 0

        for i in range(dates.shape[0]):
            date_info = dates[i].split('.')
            if len(date_info) == 3:
                d, m, y = date_info[0], date_info[1], date_info[2]
                if (len(d) == 1 or len(d) == 2) and (len(m) == 1 or len(m) == 2) and len(y) == 4:
                    day, month, year = d, m, y
                    date = datetime(int(year), int(month), int(day))
                    if start_date < date and i < index_1:
                        index_1 = i
                    if date < end_date and index_2 < i:
                        index_2 = i
        if return_output:
            return teams_values[index_1:index_2, :], dates[index_1:index_2]
        else:
            self.teams_values  = self.teams_values[index_1:index_2, :]
            self.teams_changes = self.teams_changes[index_1:index_2, :]
            self.dates  = dates[index_1:index_2]


    def plot_events(self, start_date=None, end_date=None, ylocs = [35000, 110000, 111000]):
        ymin, ymax, text_yloc = ylocs
        start_date = get_date(start_date, 'start')
        end_date = get_date(end_date, 'end')

        Events = {
            'NFL-Draft': ['30.4.2021'],
            'Draft': ['17.6.2021', 'TT'],
            'Week1': ['12.9.2021'],
            'Week2': ['19.9.2021'],
            'Week3': ['26.9.2021'],
            'Week4': ['3.10.2021'],
            'Week5': ['10.10.2021'],
            'Week6': ['17.10.2021'],
            'Week7': ['24.10.2021']
        }
        for event in Events:
            date = Events[event]
            date_datetime = get_date(date[0])

            if start_date < date_datetime and date_datetime < end_date:
                if len(date) == 2:
                    plt.plot([date[0], date[0]], [ymin, ymax], 'grey', linestyle = '--', linewidth = 0.5)
                    plt.plot([date[1], date[1]], [ymin, ymax],'grey', linestyle = '--', linewidth = 0.5)
                    plt.text(date[0], text_yloc, event, rotation='horizontal')
                else:
                    plt.plot([date[0], date[0]], [ymin, ymax], 'grey', linestyle = '--', linewidth = 0.5)
                    plt.text(date[0], text_yloc, event, rotation='vertical')

    def plot_show(self):
        plt.show()   

    def plot_save(self, plot_name):
        plt.savefig('plots/' + plot_name, dpi = 1000)

    def grid_lines(self, ymin = 0, ymax = 110000, spacing = 5000):
        #plt.minorticks_on()
        ymin = 2000*math.floor(ymin/2000)
        ymax = 2000*math.ceil(ymax/2000)
        plt.yticks(np.arange(ymin,ymax, spacing))
        plt.grid(b=True, which='major', color='grey', linestyle='--', axis = 'y')

    def grid_limits(self, ymin=35000, ymax=110000):
        ymin = 1000*math.floor(ymin/1000)
        ymax = 1000*math.ceil(ymax/1000)
        plt.ylim([ymin, ymax])

    def Adjust_Team_Values(self):
        initial_values = self.teams_changes[0,:]
        self.teams_changes -= initial_values

    def plot_team_values(self, plot_name, start_date=None, end_date=None, plot_changes_also=False):

        if start_date!=None or end_date!=None:
            self.change_time_period(
                start_date = start_date,
                end_date = end_date,
                teams_values = self.teams_values,
                dates = self.dates
            )

        self.plot_teams(
            teams_values = self.teams_values,
            dates  = self.dates,
            teams  = self.names
        )
        print(self.teams_values[-1,:])
        self.plot_events(start_date=start_date, end_date=end_date)
        self.get_xticks()
        self.grid_lines()
        self.grid_limits()
        colormaps = ['gist_earth', 'ocean', 'gnuplot', 'brg', 'rainbow', 'turbo']
        colormap = colormaps[self.colormap]
        plot_name = plot_name + ' ({})'.format(colormap)
        plt.title(plot_name, pad = 60,  fontsize = 20)
        self.plot_save(plot_name+ '.png')

        if plot_changes_also:
            self.Adjust_Team_Values()
            self.plot_teams(
                teams_values = self.teams_changes,
                dates  = self.dates,
                teams  = self.names_changes
            )
            self.plot_events(
                start_date=start_date, end_date=end_date, 
                ylocs=[
                    self.teams_changes.min()-2000, 
                    self.teams_changes.max()+2000,
                    self.teams_changes.max()+2000 + 500
                    ]
            )
            self.get_xticks()
            self.grid_lines(self.teams_changes.min()-2000, self.teams_changes.max()+2000, 2000)
            self.grid_limits(self.teams_changes.min()-2000, self.teams_changes.max()+2000)
            plt.hlines(y=0, xmin=self.dates[0], xmax=self.dates[-1], linewidth=3, color = 'black')
            plt.xlim([self.dates[0], self.dates[-1]])
            plt.title(plot_name + ' (change)', pad = 60,  fontsize = 20)
            self.plot_save(plot_name+ ' (change).png')
        print('done')



for i in range(0,6):
    obj_all = league(colormap = i)
    obj_all.plot_team_values(plot_name = 'Since Start of Measurements', plot_changes_also = False)



#obj_all = league()
#obj_all.plot_team_values(plot_name = 'Since Start of Measurements', plot_changes_also = True)
#
#obj_draft = league()
#obj_draft.plot_team_values(plot_name = 'Since 2021 Draft', start_date = '17.6.2021', plot_changes_also = True)
#
#
#obj_season = league()
#obj_season.plot_team_values(plot_name = 'Season 2021', start_date = '1.9.2021', plot_changes_also = True)


