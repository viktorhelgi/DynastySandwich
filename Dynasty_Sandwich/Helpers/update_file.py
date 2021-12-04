"""
Delete duplicates (w.r.t. dates) from
 - 'C:/Users/Lenovo/Documents/VSCode_Tests/NFL/Dynasty_Sandwich/data/keeptradecut_collection.p'

(also, History.txt later)
"""
from HelperFunctions.code_guide import PointToFunction

import pickle
import pandas as pd
import numpy as np
import os
import sys


def get_data(filename = 'C:/Users/Lenovo/Documents/VSCode_Tests/NFL/Dynasty_Sandwich/data/keeptradecut_collection.p'):
    with open(filename, 'rb') as handle:
        data = pickle.load(handle)
    return data

def create_backup():
    """Create a backup of the last dataset before updateing the dataset"""
    dir_backup = 'C:/Users/Lenovo/Documents/VSCode_Tests/NFL/Dynasty_Sandwich/data/backup/'
    files_backup = os.listdir(dir_backup)

    # get volume number of the new backup-file
    try:
        files_vol_nrs = [int(f.split('_vol')[1].split('.')[0]) for f in files_backup if ('_vol' in f) and ('.p' in f)] # -> e.g. [1, 2, 3, 4] then directory has 4 backup-files
        volume_nr_backup = max(files_vol_nrs) + 1
    except Exception as e:
        raise LookupError(f'{e}\n The error is in the code above')
    
    filename_backup = f'C:/Users/Lenovo/Documents/VSCode_Tests/NFL/Dynasty_Sandwich/data/backup/keeptradecut_collection_vol{volume_nr_backup}.p'
    data_backup = get_data(filename = 'C:/Users/Lenovo/Documents/VSCode_Tests/NFL/Dynasty_Sandwich/data/keeptradecut_collection.p')
    with open(filename_backup, 'wb') as handle:
        pickle.dump(data_backup, handle)
    print('Backup was created')

@PointToFunction()
def update__keeptradecut_collection():
    filename_main = 'C:/Users/Lenovo/Documents/VSCode_Tests/NFL/Dynasty_Sandwich/data/keeptradecut_collection.p'
    df = get_data(filename = filename_main)
    cols = df.columns
    arr = df.to_numpy()

    arr_top = arr[[i for i in range(arr.shape[0]) if arr[i,0].year == 2000],:] # keep for later
    df_top  = pd.DataFrame(arr_top, columns = cols)
    arr_bot = arr[[i for i in range(arr.shape[0]) if arr[i,0].year != 2000],:] # fix

    n_rows_before = arr_bot.shape[0]

    # remove duplicated dates
    df_bot = pd.DataFrame(arr_bot, columns = cols)
    df_bot['date_temp'] = df_bot.apply(lambda r: f"{r['Date'].year}_{r['Date'].month}_{r['Date'].day}", axis = 1)
    df_bot = df_bot.drop_duplicates(subset='date_temp', keep='last')
    df_bot = df_bot.drop('date_temp', axis = 1)

    n_rows_after = df_bot.shape[0]

    n_rows_removed = n_rows_before - n_rows_after
    Dataset_needs_updating = n_rows_removed > 0

    if Dataset_needs_updating:
        print('number of rows removed: ', n_rows_removed)
        create_backup() # create a backup before changing the dataset

        df_updated = pd.concat([df_top, df_bot])

        with open(filename_main, 'wb') as handle:
            pickle.dump(df_updated, handle)
        print('File has been updated')
    else:
        print('No rows removed')
        print('file does not need updating')


if __name__ == '__main__':
    update__keeptradecut_collection()