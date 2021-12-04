from datetime import datetime        
        
def get_date(date, end_start = 'undef'):
    if date == None:
        if end_start == 'start':
            date = datetime(1,1,1)
        elif end_start == 'end':
            date = datetime.now()
    elif type(date) == str:
        sd_info = date.split('.')
        assert len(sd_info) == 3
        date = datetime(int(sd_info[2]), int(sd_info[1]), int(sd_info[0]))
    return date