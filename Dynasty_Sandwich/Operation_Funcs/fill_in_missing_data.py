import numpy as np
import datetime

from HelperFunctions.code_guide import PointToFunction

def print_day(values, date = None):
    if date != None:
        print('{}.{}.{}'.format(date.day, date.month, date.year), end = '\t')

    for j in range(values.shape[0]):
        print(int(values[j]), end='\t')
    print('')

def fill_in_missing_data(date1, date2, vals1, vals2):
    days_to_fill = (date2-date1).days
    change = vals2 - vals1
    d_change = change/(days_to_fill)
    new_vals = np.zeros(shape=(days_to_fill-1, vals1.shape[0]))
    year, month, day = date1.year, date1.month, date1.day
    new_dates = []
    print('Output:')
    print_day(
        date=date1,
        values=vals1
    )

    for i in range(0,new_vals.shape[0]):
        new_vals[i,:] = vals1 + d_change*(i+1)
        new_dates.append(date1 + datetime.timedelta(days=i+1))

        print_day(
            values=new_vals[i,:],
            date=new_dates[i]
        )



    print_day(
        values=vals2,
        date=date2
    )
    print('')


    #combined_values = np.vstack([vals1, new_vals, vals2])
    #for i in range(1,combined_values.shape[0]):
    #    print_day(
    #        values=combined_values[i-1,:]
    #    )
    #    print_day(
    #        values=combined_values[i,:]
    #    )
    #    print_day(
    #        values=combined_values[i,:]-combined_values[i-1,:]
    #    )

def get_data(data_str):
    data_list = data_str.split('\t')
    date_str = data_list.pop(0)

    date_list = date_str.split('.')
    year, month, day = int(date_list[2]), int(date_list[1]), int(date_list[0])
    date_out = datetime.datetime(year, month, day)

    vals_out = np.array(data_list).astype('int')

    return date_out, vals_out

@PointToFunction()
def print_missing_dates(data1, data2):
#def print_missing_dates(data):
    #data1 = data['data1']
    #data2 = data['data2']
    
    date1, values_date1 = get_data(data1)
    date2, values_date2 = get_data(data2)

    fill_in_missing_data(
        date1 = date1,
        date2 = date2,
        vals1 = values_date1,
        vals2 = values_date2
    )

if __name__ == '__main__':
    data1 = '30.10.2021	94277	109796	79547	82407	65603	72900	84474	64702	53498	60146	52081	51639'
    data2 = '3.11.2021	91833	110219	78272	82794	65521	70959	87396	66625	53533	60655	50830	51117'
    print_missing_dates(data1, data2)