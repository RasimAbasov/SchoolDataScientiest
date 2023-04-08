import math
import os
import requests
import pandas as pd
import seaborn as sns
from sqlalchemy import create_engine


"""
Задание
Реализовать с помощью объектно-ориентированного подхода предыдущие 2 задания.
Создайте для каждой из задач отдельный класс, который позволяет ее решить.

"""


class DomIdLoader:
    def __init__(self):
        self.url = 'https://xn--80az8a.xn--d1aqf.xn--p1ai/%D1%81%D0%B5%D1%80%D0%B2%D0%B8%D1%81%D1%8B/api/kn/object'

    def get_data(self, offset: int = 0, limit: int = 10) -> dict:
        params = {'offset': offset,
                  'limit': limit,
                  'sortField': 'devId.devShortCleanNm',
                  'sortType': 'asc',
                  'objStatus': 0
                  }
        while True:
            response = requests.get(url=self.url, params=params)
            if response.status_code == 200:
                return response.json()['data']

    def get_total(self) -> int:
        return self.get_data()['total']

    def show_all_ids(self) -> list:
        offset = 0
        limit = 1000
        total = self.get_total()
        cnt_offset = math.ceil(total / limit)
        list_ids = []
        for i in range(0, cnt_offset + 1):
            list_obj = self.get_data(offset=offset, limit=limit)['list']
            for obj in list_obj:
                list_ids.append(obj['objId'])
            print(offset, i)
            offset = offset + limit
        return list_ids


class ObjectInfoExtractor:
    def __init__(self) -> None:
        self.url_obj = 'https://xn--80az8a.xn--d1aqf.xn--p1ai/%D1%81%D0%B5%D1%80%D0%B2%D0%B8%D1%81%D1%8B/api/object/{}'

    def get_object(self, obj_id: int) -> dict:
        while True:
            response = requests.get(url=self.url_obj.format(obj_id))
            if response.status_code == 200:
                return response.json()['data']

    def load_data(self, list_ids: list) -> list:
        all_values = []
        for index, obj_id in enumerate(list_ids):
            print(f'index: {index}, obj_id: {obj_id}')
            data = self.get_object(obj_id=obj_id)
            all_values.append(data)
        return all_values

    @staticmethod
    def df_converter(values: list) -> pd.DataFrame:
        return pd.DataFrame(data=values)


class Saver:
    def __init__(self, data: pd.DataFrame) -> None:
        self.data = data

    def save_csv(self, path: str = 'Task1_dm_rf.csv') -> None:
        self.data.to_csv(path_or_buf=path)

    def save_xl(self, path: str = 'Task1_dm_rf.xlsx') -> None:
        writer = pd.ExcelWriter(path=path, engine='xlsxwriter')
        self.data.to_excel(writer, 'Task1')
        writer.save()

    def save_sql(self, title_db: str = 'database_task1_dm_rf.db') -> None:
        self.data['developer'] = self.data['developer'].astype('str')
        self.data['quartography'] = self.data['quartography'].astype('str')
        self.data['photoRenderDTO'] = self.data['photoRenderDTO'].astype('str')
        self.data['objectTransportInfo'] = self.data['objectTransportInfo'].astype('str')
        self.data['metro'] = self.data['metro'].astype('str')
        path = os.path.dirname(__file__)
        path_to_db = os.path.join(path, title_db)
        engine = create_engine(f'sqlite:///{path_to_db}', echo=False)
        self.data.to_sql(name='DOM_RF_DATA', con=engine, index=False)
        pd.read_sql('DOM_RF_DATA', con=engine)


class Visualizer:
    def __init__(self, data: pd.DataFrame) -> None:
        self.data = data

    def make_boxplot(self, column: list, grid: bool = False, color: str = 'color'):
        self.data.boxplot(column=column, grid=grid, color=color)

    def make_heatmap(self):
        sns.heatmap(self.data, annot=True)


ids = DomIdLoader.show_all_ids
list_values = ObjectInfoExtractor.load_data(list_ids=ids)
df = ObjectInfoExtractor.df_converter(values=list_values)
Saver(data=df).save_xl()
Saver(data=df).save_csv()
