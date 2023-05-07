import os
from enum import Enum


class Urls(Enum):
    """ urls """
    def __add__(self, other):
        return self.value + other

    hh_base = "https://api.hh.ru"
    vacancies = hh_base + "/vacancies"
    vacancy = hh_base + "/vacancies/{}"
    areas = hh_base + "/areas"
    resumes = "https://hh.ru/search/resume"
    resume = "https://hh.ru/resume/{}"


class Areas(Enum):
    """ https://github.com/hhru/api/blob/master/docs/areas.md#areas """
    Moscow = 1


ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


class Dirs(Enum):
    """ Директории и файлы для проекта """
    PAGES_VACANCIES = os.path.join(ROOT_DIR, "docs", "pages_vacancies")
    VACANCIES = os.path.join(ROOT_DIR, "docs", "vacancies")
    FILE_VACANCIES_IDS = os.path.join(ROOT_DIR, "docs", "ids_vacancies.txt")
    DOCS = os.path.join(ROOT_DIR, "docs")
    PAGES_RESUMES = os.path.join(ROOT_DIR, "docs", "pages_resumes")
    RESUMES = os.path.join(ROOT_DIR, "docs", "resumes")
    FILE_RESUMES_IDS = os.path.join(ROOT_DIR, "docs", "ids_resumes.txt")


HEADER_USER_AGENT = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/110.0.0.0 Safari/537.36'
                     }
