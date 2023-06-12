import pandas as pd
from home.models import Varandma

df = pd.read_csv('home/df_varandma.csv')

set_yeak = ['แยกสามย่าน', 'แยกอังรีดูนังค์', 'แยกศาลาแดง'] + ['แยกสามย่าน', 'แยกอังรีดูนังค์', 'แยกศาลาแดง', 'แยกราชดำริ'] + ['แยกสามย่าน', 'แยกอังรีดูนังค์', 'แยกศาลาแดง', 'แยกวิทยุ', 'แยกคลองเตย', 'แยกพระรามที่ 4'] + ['แยกศาลาแดง', 'แยกราชดำริ'] + ['แยกศาลาแดง', 'แยกวิทยุ', 'แยกคลองเตย', 'แยกพระรามที่ 4'] + ['แยกราชดำริ', 'แยกศาลาแดง', 'แยกวิทยุ', 'แยกคลองเตย', 'แยกพระรามที่ 4']
yeak = list(set(set_yeak))
df_only_from = pd.DataFrame()
df_only = pd.DataFrame()
for e in yeak:
    df_only_temp = df[df['from'] == e]
    df_only_from = pd.concat([df_only_from, df_only_temp], axis=0)

for e in yeak:
    df_only_temp = df_only_from[df_only_from['end'] == e]
    df_only = pd.concat([df_only, df_only_temp], axis=0)

for i,row in df_only.iterrows():
    print(i)
    Varandma(From=row['from'], End=row['end'], days=row['days'], time=row['time'], ff=row['freeflow traveltime'], avg=row['average traveltime'], p95=row['95th percentile'], tti=row['Traveltime Index'], year=row['year']).save()