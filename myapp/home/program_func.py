import datetime
import matplotlib
matplotlib.use('Agg')
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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
        return 0
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

    avg_time = 0    # buffer index = 0%
    plan_time = 0   # buffer index = 100% (95th percentile)

    a = line[route]
    for i in range(len(a)-1):
        temp = df[(df['from']==a[i]) & (df['end']==a[i+1]) & (df['days']==day) & (df['time']==time)]
        # ptime += temp['Planningtime'].mean() + 180 # planning time (95th percentile)
        avg_time += temp['average traveltime'].mean() + 180 # +180 คือบวกไฟแดงละ 3 นาที
        plan_time += temp['Planningtime']
    if avg_time == np.nan:
        return 0
    return [avg_time/60, plan_time]

# print(round(float(query_time('sm_qs'))))

def query_visual_tti(day, time):
    df = pd.read_csv('home/df_varandma.csv')
    df = df.query(f'days == "{day}" and time == "{time}"')
    return df.head()


def buffer_index(time, percent):
    return (percent/100)*time

def value_pie(pct, all_val):
    absolute = int((pct/100)*all_val)
    return f'{absolute:d} min'


def pie_chart(time, percent, filename):
    buffer = buffer_index(time, percent)
    data = [time, buffer]
    color = ['#47A6AB', '#E54450']
    explode = (0.01, 0.01)
    plt.pie(data, colors=color, explode=explode, labels=['Average', 'Extra'], 
            autopct=lambda pct: value_pie(pct, time+buffer), pctdistance=0.85)
    center_circle = plt.Circle((0, 0), 0.7, fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(center_circle)
    plt.savefig(f'home/chart_img/pie_({filename}).png')
    # plt.show()
    plt.close()