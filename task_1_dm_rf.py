import math
import os
import requests
import pandas as pd
from sqlalchemy import create_engine

""" Задание:
        Собрать информацию о всех строящихся объектах на сайте "наш.дом.рф"
        Cохранить ее в pandas dataframe
        Cохранить pandas dataframe в excel
        Cохранить pandas dataframe в pickle
        Cохранить pandas dataframe в БД """


def get_houses_under_construction(offset: int = 0, limit: int = 10) -> tuple:
    """ Получение строющихся домов """
    url = f'https://xn--80az8a.xn--d1aqf.xn--p1ai/%D1%81%D0%B5%D1%80%D0%B2%D0%B8%D1%81%D1%8B/api/kn/object'
    params = {'offset': offset,
              'limit': limit,
              'sortField': 'devId.devShortCleanNm',
              'sortType': 'asc',
              'objStatus': 0
              }
    status_code = None
    while status_code != 200:
        response = requests.get(url=url, params=params)
        status_code = response.status_code
    res_total = response.json()['data']['total']
    houses = response.json()['data']['list']
    return houses, res_total


_, total = get_houses_under_construction()
# Округляем количество страниц с данными по домам (всего записей 10781, делим на limit) и находим количество страниц
offset = 0
limit = 1000
cnt_offset = math.ceil(total / limit)
cnt_req = []
for i in range(0, cnt_offset + 1):
    lst_houses, _ = get_houses_under_construction(offset=offset, limit=limit)
    print(offset, i)
    cnt_req.append(lst_houses)
    offset = offset + limit

list_values = sum(cnt_req, [])
df = pd.DataFrame(data=list_values)

# Save DataFrame to excel
writer = pd.ExcelWriter('Task1_dm_rf.xlsx', engine='xlsxwriter')
df.to_excel(writer, 'Task1')
writer.save()

# Save DataFrame to pickle
df.to_pickle('Task1_dm_rf.pkl')

# Save DataFrame to DB
df = pd.read_pickle('Task1_dm_rf.pkl')
# change type column developer
df['developer'] = df['developer'].astype('str')
path = os.path.dirname(__file__)
path_to_db = os.path.join(path, 'database_task1_dm_rf.db')
engine = create_engine(f'sqlite:///{path_to_db}', echo=False)
df.to_sql(name='DOM_RF_DATA', con=engine, index=False)
df_from_db = pd.read_sql('DOM_RF_DATA', con=engine)
