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


def get_data(offset: int = 0, limit: int = 10) -> dict:
    """ Получение строющихся домов """
    url = f'https://xn--80az8a.xn--d1aqf.xn--p1ai/%D1%81%D0%B5%D1%80%D0%B2%D0%B8%D1%81%D1%8B/api/kn/object'
    params = {'offset': offset,
              'limit': limit,
              'sortField': 'devId.devShortCleanNm',
              'sortType': 'asc',
              'objStatus': 0
              }
    while True:
        response = requests.get(url=url, params=params)
        if response.status_code == 200:
            return response.json()['data']


def get_object(obj_id: int) -> dict:
    url = f'https://xn--80az8a.xn--d1aqf.xn--p1ai/%D1%81%D0%B5%D1%80%D0%B2%D0%B8%D1%81%D1%8B/api/object/{obj_id}'
    while True:
        response = requests.get(url=url)
        if response.status_code == 200:
            return response.json()['data']


def get_total() -> int:
    return get_data()['total']


def get_ids_obj() -> list:
    # Округляем количество страниц с данными по домам (всего записей 10781, делим на limit) и находим количество страниц
    offset = 0
    limit = 1000
    total = get_total()
    cnt_offset = math.ceil(total / limit)
    ids = []
    for i in range(0, cnt_offset + 1):
        list_obj = get_data(offset=offset, limit=limit)['list']
        for obj in list_obj:
            ids.append(obj['objId'])
        print(offset, i)
        offset = offset + limit
    return ids


obj_ids = get_ids_obj()


def get_all_objects(ids: list):
    all_values = []
    for index, obj_id in enumerate(ids):
        print(index, obj_id)
        data = get_object(obj_id=obj_id)
        all_values.append(data)
    return all_values


list_values = get_all_objects(ids=obj_ids)
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
