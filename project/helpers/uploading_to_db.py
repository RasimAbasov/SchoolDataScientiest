import pandas as pd

import json
import os
from sqlalchemy import create_engine
from collections import defaultdict


class UploadToDB:
    """ Загрузка вакансий в базу данных """
    def __init__(self) -> None:
        self.vacancies = os.path.normpath(os.path.join(os.getcwd(), "docs", "vacancies"))
        self.path_to_db = os.path.normpath(os.path.join(os.getcwd(), "docs"))

    def fill_dicts(self) -> tuple[dict, dict]:
        data_vacancies = defaultdict(list)
        data_skills = defaultdict(list)
        for file_vacancy in os.listdir(self.vacancies):

            # Открываем, читаем и закрываем файл.
            f = open(os.path.join(self.vacancies, file_vacancy), encoding="utf8")
            json_text = f.read()
            f.close()

            # Текст файла переводим в json
            vacancy = json.loads(json_text)

            # Заполняем словарь идентификаторами вакансий, наименованиями, описаниями, навыками.
            data_vacancies["id"].append(vacancy["id"])
            data_vacancies["name"].append(vacancy["name"])
            data_vacancies["description"].append(vacancy["description"])
            # data_dict["skills"].append(vacancy.get("key_skills"))
            # sk = data_dict.get("skills")
            # data_dict["skills"] = [",".join([y.get("name") for y in x]) for x in sk]

            # Т.к. навыки хранятся в виде массива, то проходимся по нему циклом.
            for skil in vacancy['key_skills']:
                data_skills["id"].append(vacancy["id"])
                data_skills["name"].append(skil["name"])
        return data_vacancies, data_skills

    @staticmethod
    def make_dataframe(data_dict: dict) -> pd.DataFrame:
        # Создание DataFrame из словаря.
        return pd.DataFrame(data=data_dict)

    def create_db(self, data_frame: pd.DataFrame, name_db: str) -> None:
        path = os.path.join(self.path_to_db, f"{name_db}.db")
        engine = create_engine(f"sqlite:///{path}", echo=False)
        connect = engine.connect()
        data_frame.to_sql(name=name_db, con=connect, index=False)
        connect.close()

    def create_dfs(self) -> tuple[pd.DataFrame, pd.DataFrame]:
        data_vacancies, data_skills = self.fill_dicts()
        df_vacancies = self.make_dataframe(data_dict=data_vacancies)
        df_skills = self.make_dataframe(data_dict=data_skills)
        return df_vacancies, df_skills

