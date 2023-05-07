from project.helpers.uploading_to_db import UploadToDB

# Сохранение резюме в БД

upload_to_db = UploadToDB()
df_resumes = upload_to_db.create_df_resumes()
upload_to_db.create_db(data_frame=df_resumes, name_db="resumes")
