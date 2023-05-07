from project.helpers.uploading_to_db import UploadToDB

# Сохранение вакансий в БД

upload_to_db = UploadToDB()
df_vacancies, df_skills = upload_to_db.create_dfs_vacancies()
upload_to_db.create_db(data_frame=df_vacancies, name_db="vacancies")
upload_to_db.create_db(data_frame=df_skills, name_db="skills")
