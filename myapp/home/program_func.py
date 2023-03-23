import datetime
import matplotlib
matplotlib.use('Agg')
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

def index_time(time, percent):
    pass

def diff(d2):
    import datetime
    day = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
    d1 = datetime.date(2018,12,30)
    delta = d2-d1
    c = delta.days%7
    return day[c]

def s_name(name):
    name = name.split()
    text = name[0][0]+name[1][0]
    text = text.lower()
    return text

def query_time(route, dt):
    if route[0:2] == route[3:]:
        return {'ff_time':0, 'avg_time':0, 'p95_time':0}
    line = {
        'sm_ch': ['แยกสามย่าน', 'แยกอังรีดูนังค์', 'แยกศาลาแดง'],
        'sm_lp': ['แยกสามย่าน', 'แยกอังรีดูนังค์', 'แยกศาลาแดง', 'แยกราชดำริ'],
        'sm_qs': ['แยกสามย่าน', 'แยกอังรีดูนังค์', 'แยกศาลาแดง', 'แยกวิทยุ', 'แยกคลองเตย', 'แยกพระรามที่ 4'],
        'ch_sm': ['แยกสามย่าน', 'แยกอังรีดูนังค์', 'แยกศาลาแดง'][-1::-1],
        'ch_lp': ['แยกศาลาแดง', 'แยกราชดำริ'],
        'ch_qs': ['แยกศาลาแดง', 'แยกวิทยุ', 'แยกคลองเตย', 'แยกพระรามที่ 4'],
        'lp_sm': ['แยกสามย่าน', 'แยกอังรีดูนังค์', 'แยกศาลาแดง', 'แยกราชดำริ'][-1::-1],
        'lp_ch': ['แยกศาลาแดง', 'แยกราชดำริ'][-1::-1],
        'lp_qs': ['แยกราชดำริ', 'แยกศาลาแดง', 'แยกวิทยุ', 'แยกคลองเตย', 'แยกพระรามที่ 4'],
        'qs_sm': ['แยกสามย่าน', 'แยกอังรีดูนังค์', 'แยกศาลาแดง', 'แยกวิทยุ', 'แยกคลองเตย', 'แยกพระรามที่ 4'][-1::-1],
        'qs_ch': ['แยกศาลาแดง', 'แยกวิทยุ', 'แยกคลองเตย', 'แยกพระรามที่ 4'][-1::-1],
        'qs_lp': ['แยกราชดำริ', 'แยกศาลาแดง', 'แยกวิทยุ', 'แยกคลองเตย', 'แยกพระรามที่ 4'][-1::-1]
    }
    df = pd.read_csv('home/df_varandma.csv')
    # dt = datetime.datetime.now()
    time = dt.strftime("%H:%M:%S")
    time = time[:4]+'0:00'
    dt = pd.to_datetime(dt)
    day = diff(dt.date())

    ff_time = 0
    avg_time = 0 
    p95_time = 0
    tti = []

    a = line[route]
    for i in range(len(a)-1):
        temp = df[(df['from']==a[i]) & (df['end']==a[i+1]) & (df['days']==day) & (df['time']==time)]
        ff_time += temp['freeflow traveltime'].mean() # free flow
        avg_time += temp['average traveltime'].mean() # average
        p95_time += temp['95th percentile'].mean() # 95th percentile
        tti.append(temp['Traveltime Index'].mean())
    tti = sum(tti)/len(tti)
    
    if not math.isnan(ff_time) or not math.isnan(avg_time) or not math.isnan(p95_time) or math.isnan(tti):
        return {'ff_time':round(ff_time), 'avg_time':round(avg_time), 'p95_time':round(p95_time), 'tti':tti}
    else:
        return {'ff_time':0, 'avg_time':0, 'p95_time':0}#, 'tti':0}

def graph_time(og, ds, time):
    set_time = {'time':[], 'tti':[], 'Unsafe':[], 'Usual':[], 'Safe':[]}
    # set_time = {'time':[], 'Unsafe':[], 'Usual':[], 'Safe':[]}
    start = f'{str(time)[:10]} 10:00:00'
    start = pd.to_datetime(start)
    stop = f'{str(time)[:10]} 21:00:00'
    stop = pd.to_datetime(stop)
    delta = datetime.timedelta(hours=1)
    while start <= stop:
        time = query_time(route=f'{s_name(og)}_{s_name(ds)}', dt=start)
        set_time['time'].append(start.strftime('%H:%M'))
        set_time['Unsafe'].append(time['ff_time'])
        set_time['Usual'].append(time['avg_time'])
        set_time['Safe'].append(time['p95_time'])
        set_time['tti'].append(time['tti'])
        start += delta
    return set_time

# print(graph_time('S M', 'C h', datetime.datetime.now()))
