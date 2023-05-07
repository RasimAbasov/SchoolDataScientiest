import os
import re
from http import HTTPStatus

import requests

from project.helpers.variables import Areas
from project.helpers.variables import Dirs
from project.helpers.variables import HEADER_USER_AGENT
from project.helpers.variables import Urls


# https://github.com/hhru/api/blob/master/docs/employer_resumes.md
# https://github.com/hhru/api/blob/master/docs/resumes_search.md
# Доступ к API для резюме платный, открываем страницу и регулярным выражением находим id резюме


class ResumeLoader:
    """ Class для выгрузки резюме """
    
    @staticmethod
    def get_page(date_from: str,
                 date_to: str, 
                 text_filter: str | None = None,
                 area: Areas = Areas.Moscow,
                 count_on_page: int = 50,
                 page: int = 1) -> str:
        """
        Метод для получения страницы со списком резюме
        Args:
            date_from: дата публикации "от"
            date_to: дата публикации "до"
            text_filter: ключевые слова для поиска
            area: регион
            count_on_page: количество элементов на странице
            page: номер страницы

        Returns: страница с резюме

        """

        params = {
            "text": text_filter,
            "area": area.value,
            "date_from": date_from,
            "date_to": date_to,
            "items_on_page": count_on_page,
            "page": page,
            "isDefaultArea": "true",
            "pos": "full_text",
            "logic": "normal",
            # "exp_period": "all_time",
            "ored_clusters": "true",
            "order_by": "relevance",
            "exp_company_size": "any",
            "exp_industry": "any"
        }
        session = requests.session()
        response = session.get(url=Urls.resumes.value, params=params, headers=HEADER_USER_AGENT)
        assert response.status_code == HTTPStatus.OK, \
            f"Ожидаемый статус ответа: {HTTPStatus.OK}, фактический: {response.status_code}, response: {response.text}"
        response.close()
        return response.content.decode("utf-8")

    def get_all_resumes(self, date_from: str, date_to: str) -> None:
        """
        Функция сохраняет резюме со страницы в файл, полученные после запроса
        Args:
            date_from: дата публикации "от"
            date_to: дата публикации "до"

        """
        count_pages = 99
        # Создаем папку, на случай ее отсутствия
        os.makedirs(name=Dirs.PAGES_RESUMES.value, exist_ok=True)
        for page in range(1, count_pages + 1):
            data = self.get_page(page=page, date_from=date_from, date_to=date_to)
            path = os.path.join(Dirs.PAGES_RESUMES.value, f"page_{page}_{date_from.replace(':', '-')}.html")
            print(f"page_{page}_{date_from}-{date_to}")
            f = open(file=path, mode="w", encoding="utf-8")
            f.write(data)
            f.close()

    @staticmethod
    def get_resume(resume_id: int | str) -> str:
        """
        Открываем страницу и получаем детальную информацию по конкретному резюме
        Args:
            resume_id: id резюме

        Returns:
            Данные по резюме
        """
        session = requests.session()
        response = session.get(url=Urls.resume.value.format(resume_id), headers=HEADER_USER_AGENT)
        response.close()
        assert response.status_code == HTTPStatus.OK, \
            f"Ожидаемый статус ответа: {HTTPStatus.OK}, фактический: {response.status_code}, response: {response.text}"
        return response.content.decode("utf-8")

    @staticmethod
    def get_resume_id_from_pages():
        """
        Получаем перечень ранее созданных файлов в pages со списков резюме и проходимся по нему в цикле,
        сохраняем содержимое

        """
        for file in os.listdir(path=Dirs.PAGES_RESUMES.value):
            f = open(file=os.path.join(Dirs.PAGES_RESUMES.value, file), encoding="utf-8")
            html_text = f.read()
            f.close()
            end_file = open(file=Dirs.FILE_RESUMES_IDS.value, mode="a+", encoding="utf-8")
            # Вытаскиваем id резюме со ссылки.
            regex = r'href="/resume/(.+?)\?hhtmFrom=resume_search_result"'
            matches = re.findall(regex, html_text)
            for value in matches:
                # Записываем все id резюме в один файл.
                end_file.write(f"{value}\n")
            end_file.close()

    def write_resume_in_file(self) -> None:
        """
        Функция сохраняет данные по резюме в файл

        """
        # Создаем папку, на случай ее отсутствия
        os.makedirs(name=Dirs.RESUMES.value, exist_ok=True)
        f = open(file=Dirs.FILE_RESUMES_IDS.value, encoding="utf-8")
        text = f.read()
        f.close()
        list_ids = text.split("\n")[:-1]
        for resume_id in list_ids:
            file_name = f"id_{resume_id}.html"
            if file_name not in os.listdir(path=Dirs.RESUMES.value):
                file_path = os.path.join(Dirs.RESUMES.value, file_name)
                print(file_name)
                response = self.get_resume(resume_id=resume_id)
                f = open(file=file_path, mode="w", encoding="utf-8")
                f.write(response)
                f.close()
