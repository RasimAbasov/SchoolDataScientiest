
from enum import Enum


class Urls(Enum):
    """ urls """
    def __add__(self, other):
        return self.value + other

    hh_base = "https://api.hh.ru"
    vacancies = hh_base + "/vacancies"
    areas = hh_base + "/areas"


class Areas(Enum):
    """ https://github.com/hhru/api/blob/master/docs/areas.md#areas """
    Moscow = 1


