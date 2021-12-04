import os


def get_file_name():
    path = 'C:/Users/Lenovo/Documents/nfl/'


    for i,j,k in os.walk(path):
        files = k
        break

    file_nrs = []
    for file in files:
        if 'Automatic_with_macros' in file:
            file_split = file.split('Automatic_with_macros_vol')
            if len(file_split) == 2:
                file_nr = file_split[1].split('.')[0]
                if file_nr.isdigit():
                    file_nrs.append(int(file_nr))
        
    file_vol = max(file_nrs)

    file_name = 'Automatic_with_macros_vol'+str(file_vol)+'.xlsm'
    assert file_name in files, 'file [{}] not in files'.format(file_name)
    return path + file_name
