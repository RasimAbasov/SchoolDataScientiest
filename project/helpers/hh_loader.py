import json
import math
import os
from http import HTTPStatus

import requests

from project.helpers.variables import Urls, Areas


class HHLoader:
    """ Class для выгрузки вакансий """
    def __init__(self, text_filter: str | None = None,
                 area: Areas = Areas.Moscow, count_vacancies_on_page: int = 100) -> None:
        self.text_filter = text_filter
        self.area = area.value,
        self.count_vacancies_on_page = count_vacancies_on_page

    @staticmethod
    def get_areas() -> dict:
        """
        Метод получает дерево регионов
        Returns: словарь кодов регионов

        """
        response = requests.get(url=Urls.areas.value)
        assert response.status_code == HTTPStatus.OK, \
            f"Ожидаемый статус ответа: {HTTPStatus.OK}, фактический: {response.status_code}"
        return response.json()

    def get_page(self, date_from: str, date_to: str, page: int = 0) -> dict:
        """
        Метод для получения страницы со списком вакансий
        Args:
            date_from: дата публикации "от"
            date_to: дата публикации "до"
            page: номер страницы

        Returns: словарь с вакансиями

        """

        params = {
            "text": self.text_filter,
            "area": self.area,
            "page": page,
            "per_page": self.count_vacancies_on_page,
            "date_from": date_from,
            "date_to": date_to
        }
        response = requests.get(url=Urls.vacancies.value, params=params)
        assert response.status_code == HTTPStatus.OK, \
            f"Ожидаемый статус ответа: {HTTPStatus.OK}, фактический: {response.status_code}, response: {response.text}"
        response.close()
        return response.json()

    def get_all_found(self, date_from: str, date_to: str) -> int:
        """

        Args:
            date_from: дата публикации "от"
            date_to: дата публикации "до"

        Returns: общее количество вакансий в промежутке от и до

        """
        return self.get_page(date_from=date_from, date_to=date_to)['found']

    def get_all_vacancies(self, date_from: str, date_to: str) -> None:
        """

        Args:
            date_from: дата публикации "от"
            date_to: дата публикации "до"

        Returns:

        """
        all_vacancies = self.get_all_found(date_from=date_from, date_to=date_to)
        count_pages = math.ceil(all_vacancies / self.count_vacancies_on_page)
        for page in range(0, count_pages + 1):
            data = self.get_page(page=page, date_from=date_from, date_to=date_to)
            if data['items']:
                path = os.path.normpath(os.path.join(os.getcwd(), "docs", "pagination",
                                                     f"page_{page}_{date_from.replace(':', '-')}.json"))
                print(f'page_{page}_{date_from}-{date_to}')

                f = open(file=path, mode='w', encoding='utf-8')
                f.write(json.dumps(obj=data, ensure_ascii=False))
                f.close()

    @staticmethod
    def get_vacancy(vacancy_id: int) -> dict:
        # Обращаемся к API и получаем детальную информацию по конкретной вакансии
        response = requests.get(url=Urls.vacancy.value.format(vacancy_id))
        assert response.status_code == HTTPStatus.OK, \
            f"Ожидаемый статус ответа: {HTTPStatus.OK}, фактический: {response.status_code}, response: {response.text}"
        response.close()
        return response.json()

    def upload_vacancy_in_file(self):
        """
        Получаем перечень ранее созданных файлов в pagination со списком вакансий и проходимся по нему в цикле,
        сохраняем содержимое
        Returns:

        """

        pagination = os.path.normpath(os.path.join(os.getcwd(), "docs", "pagination"))
        vacancies = os.path.normpath(os.path.join(os.getcwd(), "docs", "vacancies"))
        for file in os.listdir(pagination):
            f = open(file=os.path.join(pagination, file), encoding='utf-8')
            json_text = f.read()
            f.close()

            json_obj = json.loads(json_text)

            # Получаем и проходимся по непосредственно списку вакансий
            for value in json_obj['items']:
                data = self.get_vacancy(vacancy_id=value['id'])
                # Создаем файл в формате json с идентификатором вакансии в качестве названия.
                # Записываем в него ответ запроса и закрываем файл.
                file_name = os.path.join(vacancies, f"id_{value['id']}.json")
                f = open(file=file_name, mode='w', encoding='utf-8')
                f.write(json.dumps(obj=data, ensure_ascii=False))
                f.close()
