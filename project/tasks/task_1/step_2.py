from project.helpers.hh_vacancy_loader import VacancyLoader

# Сохраняем данные по конкретным вакансиям после выгрузки по страницам

loader = VacancyLoader()
loader.get_vacancy_id_from_pages()
loader.write_vacancy_in_file()
