from Dynasty_Sandwich.api_sleeper_team_info import sleeper_calculate
from Dynasty_Sandwich.keeptradecut import update_keeptradecut
from Dynasty_Sandwich.visualize_excel import plot_history
import time
import ctypes  # An included library with Python install.   
from datetime import datetime



def log_status(location):
    with open('Dynasty_Sandwich/Journal_tasks.txt', 'a') as f:
        if location==0:
            date = datetime.now()
            f.write('\n{}.{}.{}\t'.format(date.day, date.month, date.year))
            f.write('| Job has started | >> ')
        elif location==1:
            f.write('| update_keeptradecut() finished | >> ' )
        elif location==2:
            f.write('| sleeper_calculate() finished | >> ')
        elif location==3:
            f.write('| plot_history() finished | >> ')
        elif location==-1:
            f.write('| Job has ended |')

def main():
    #time.sleep(10)
    update_keeptradecut()
    log_status(1)
    sleeper_calculate(update = True)
    log_status(2)

    #plot_history()
    #log_status(3)
    
if __name__ == '__main__':
    log_status(0)
    main()
    log_status(-1)
    print('Success')

