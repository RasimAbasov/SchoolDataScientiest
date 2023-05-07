import json
import os
import re
from collections import defaultdict

import pandas as pd
from sqlalchemy import create_engine

from project.helpers.variables import Dirs


class UploadToDB:
    """ Загрузка вакансий и резюме в БД """
    def __init__(self) -> None:
        self.vacancies = Dirs.VACANCIES.value
        self.resumes = Dirs.RESUMES.value
        self.path_to_db = Dirs.DOCS.value

    def fill_dicts_vacancies(self) -> tuple[dict, dict]:
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

    def create_dfs_vacancies(self) -> tuple[pd.DataFrame, pd.DataFrame]:
        data_vacancies, data_skills = self.fill_dicts_vacancies()
        df_vacancies = self.make_dataframe(data_dict=data_vacancies)
        df_skills = self.make_dataframe(data_dict=data_skills)
        return df_vacancies, df_skills

    def fill_dicts_resumes(self) -> dict:
        data_resumes = defaultdict(list)
        for file_resume in os.listdir(self.resumes):
            # Открываем, читаем и закрываем файл.
            f = open(os.path.join(self.resumes, file_resume), encoding="utf8")
            html_text = f.read()
            f.close()
            print(file_resume)

            # regex = r'href="https://hh.ru/resume/(.+?)"'
            # resume_id = re.findall(regex, html_text)[0]

            regex = r'id_(.+?)\.html'
            resume_id = re.findall(regex, file_resume)[0]

            regex = r'data-qa="resume-block-title-position">(.+?)</span>'
            lst_resume_title = re.findall(regex, html_text)

            regex = r'data-qa="resume-block-experience-description">(.+?)</div>'
            resume_experience = re.findall(regex, html_text)
            # Объединить весь опыт работы в одну строку.
            if lst_resume_title and resume_experience:
                text_experience = ','.join(s for s in resume_experience)
                data_resumes["id"].append(resume_id)
                data_resumes["title"].append(lst_resume_title[0])
                data_resumes["experience"].append(text_experience)
        return data_resumes

    def create_df_resumes(self) -> pd.DataFrame:
        data = self.fill_dicts_resumes()
        df_resumes = self.make_dataframe(data_dict=data)
        return df_resumes
