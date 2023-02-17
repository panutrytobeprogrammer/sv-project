import datetime
import pandas as pd

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

    ptime = 0
    a = line[route]
    for i in range(len(a)-1):
        temp = df[(df['from']==a[i]) & (df['end']==a[i+1]) & (df['days']==day) & (df['time']==time)]
        ptime += temp['Planningtime'].mean()

    return ptime

# print(round(float(query_time('sm_qs'))))