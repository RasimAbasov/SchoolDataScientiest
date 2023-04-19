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
        Returns:

        """
        response = requests.get(url=Urls.areas.value)
        assert response.status_code == HTTPStatus.OK, \
            f"Ожидаемый статус ответа: {HTTPStatus.OK}, фактический: {response.status_code}"
        return response.json()

    def get_page(self, date_from, date_to, page: int = 0) -> dict:
        """
        Метод для получения страницы со списком вакансий
        Returns:

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

    def get_all_found(self, date_from, date_to) -> int:
        """

        Returns:

        """
        return self.get_page(date_from=date_from, date_to=date_to)['found']

    def get_all_vacancies(self, date_from, date_to):
        all_vacancies = self.get_all_found(date_from=date_from, date_to=date_to)
        count_pages = math.ceil(all_vacancies / self.count_vacancies_on_page)
        for page in range(0, count_pages + 1):
            data = self.get_page(page=page, date_from=date_from, date_to=date_to)
            if data['items'] is not None:
                path = os.path.normpath(os.path.join(os.getcwd(), "docs", "pagination",
                                                     f"page_{page}_{date_from.replace(':', '-')}.json"))
                print(f'page_{page}_{date_from}-{date_to}')
                # Создаем новый документ, записываем в него ответ запроса, после закрываем
                f = open(path, mode='w', encoding='utf8')
                f.write(json.dumps(data, ensure_ascii=False))
                f.close()
