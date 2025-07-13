#!/usr/bin/env python3
from datetime import date, timedelta

start = date(1980, 1, 1)
end = date.today()

with open('date_wordlist.txt', 'w') as f:
    d = start
    while d <= end:
        ymd = d.strftime('%Y%m%d')
        ymd_dash = d.strftime('%Y-%m-%d')
        dmy_dot = d.strftime('%d.%m.%Y')
        dmy_dash = d.strftime('%d-%m-%Y')
        dmy = d.strftime('%d%m%Y')
        f.write(f"{ymd}\n{ymd_dash}\n{dmy_dot}\n{dmy_dash}\n{dmy}\n")
        d += timedelta(days=1)
