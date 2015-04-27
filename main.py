import re
import subprocess
import urllib.request
import datetime

def search(data_dict):
    engine = 'http://www.assembly.ab.ca/documents/isysmenu.html'
    
    data_items = []
    for n, v in data_dict.items():
        data_items.append('='.join((n, v)))
    
    data = '&'.join(data_items).encode('ascii')
    r = urllib.request.urlopen(engine, data)
    
    return r

def get_hansard_obj(date):
    fdate = date.strftime('%Y%m%d')
    ftime = date.strftime('%H%M')
    
    fname = '_'.join((fdate, ftime, '01_han.pdf'))
    
    data_dict = {'IW_DATABASE': 'i_hansards',
                 'IW_FIELD_INPUT': 'Title',
                 'IW_FILTER_FNAME_LIKE': fname,
                 'IW_FIELD_OK': 'Search+in+Hansard'}
    
    return search(data_dict)
    
def process_hansard(html_obj):
    return None
    
if __name__ == '__main__':
    year = int(input('year: '))
    month = int(input('month: '))
    day = int(input('day: '))
    time = input('time (morning/afternoon/evening): ')
    
    if time == 'morning':
        time = datetime.time(8, 30)
    elif time == 'afternoon':
        time = datetime.time(13, 30)
    else:
        time = datetime.time(19, 30)
    
    date = datetime.datetime.combine(datetime.date(year, month, day), time)
    print(get_hansard_obj(date).read())
