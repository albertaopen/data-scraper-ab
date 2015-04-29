#!/usr/bin/env python3

# Copyright (c) 2015 Zhan Tong Zhang
# Data scraper for Alberta Hansard
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

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
    res = r.read()
    url = r.geturl()
    r.close()

    return [res, url]


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
    html = str(html_obj).replace(r'\r\n', '\n')

    # remove useless information (styles and mail-in info)
    content = re.split('html>[\s\S]*(?=Province of Alberta<br \/>)', html)
    content = re.split(r'If your address is incorrect',
                       content[1])[0].replace('<br />', '\n')
    with open('output.txt', 'w') as file:
        file.write(content)

    start = re.search(r'\[The Speaker in the chair\]', content)
    end = re.search('Table of Contents', content)

    print(content)

    return None

if __name__ == '__main__':
    year = int(input('year: '))
    month = int(input('month: '))
    day = int(input('day: '))
    time = input('time (morning/afternoon/evening): ')

    if time == 'morning' or time == 'm':
        time = datetime.time(8, 30)
    elif time == 'afternoon' or time == 'a':
        time = datetime.time(13, 30)
    else:
        time = datetime.time(19, 30)

    date = datetime.datetime.combine(datetime.date(year, month, day), time)
    obj = get_hansard_obj(date)
    print(obj[1])
    process_hansard(obj[0])
