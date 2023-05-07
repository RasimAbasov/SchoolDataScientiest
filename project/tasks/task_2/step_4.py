import os

import pandas as pd
from sqlalchemy import create_engine

from project.helpers.transform import Transform
from project.helpers.uploading_to_db import UploadToDB

# Предообработать текст описаний вакансий (токенизировать, привести к нормальной форме)


upload_to_db = UploadToDB()
transform = Transform()

path_vacancies = os.path.join(upload_to_db.path_to_db, "vacancies.db")
conn = create_engine(f"sqlite:///{path_vacancies}").connect()
df = pd.read_sql('vacancies', con=conn)
conn.close()
df['lemmatized_text'] = df['description'].apply(lambda x: transform.text_transform(text=x))

upload_to_db.create_db(data_frame=df, name_db="lemmatized_text")
