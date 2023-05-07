from project.helpers.hh_resume_loader import ResumeLoader

# Сохраняем данные по конкретным резюме после выгрузки по страницам


loader = ResumeLoader()
loader.get_resume_id_from_pages()
loader.write_resume_in_file()
