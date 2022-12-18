import math
import time

import requests
import pandas as pd

""" Задание:
        Собрать информацию о всех строящихся объектах на сайте "наш.дом.рф"
        Cохранить ее в pandas dataframe
        Cохранить pandas dataframe в excel
        Cохранить pandas dataframe в pickle
        Cохранить pandas dataframe в БД """


def get_houses_under_construction(offset: int = 0, limit: int = 10) -> tuple:
    """ Получение строящихся домов"""
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
    assert status_code == 200, f'Ошибка в выполнении запроса: {response.text}'
    res_total = response.json()['data']['total']
    houses = response.json()['data']['list']
    return houses, res_total


list_houses, total = get_houses_under_construction()
# keys = list(list_houses[0].keys())

# Округляем количество страниц с данными по домам (всего записей 10781, делим на limit) и находим количество страниц
offset = 0
limit = 1000
cnt_offset = math.ceil(total / limit)
list_values = []
for i in range(0, cnt_offset + 1):
    lst_houses, _ = get_houses_under_construction(offset=offset, limit=limit)
    print(offset, i)
    list_values.append(lst_houses)
    offset = offset + limit
    # time.sleep(10)

print()
# df = pd.DataFrame(data=list_values, columns=keys)

# Specify a writer
writer = pd.ExcelWriter('Task1_dmrf.xlsx', engine='xlsxwriter')

# Write your DataFrame to a file
# df.to_excel(writer, 'Task1')

# Save the result
writer.save()