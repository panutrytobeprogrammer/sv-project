# import pandas as pd
# from .models import Varandma

df = pd.read_csv('home/df_varandma.csv')
for i,row in df.iterrows():
    From = row['from']
    End = row['end']
    days = row['days']
    time = row['time']
    ff = row['freeflow traveltime']
    avg = row['average traveltime']
    p95 = row['95th percentile']
    tti = row['Traveltime Index']
    year = row['year']
    Varandma(From=From, End=End, days=days, time=time, ff=ff, avg=avg, p95=p95, tti=tti, year=year).save()