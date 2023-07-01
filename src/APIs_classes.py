from abc import ABC, abstractmethod
import requests
import os
from saver import JSONSaver


class BaseAPI(ABC):

    @abstractmethod
    def get_vacancies(self, keyword, page):
        pass

    @staticmethod
    def get_json_saver(filename):
        return JSONSaver(filename)


class HH_API(BaseAPI):

    def __init__(self):
        self.url = 'https://api.hh.ru/vacancies'

    def get_vacancies(self, keyword, page=0):
        params = {
            'text': keyword,
            'page': page
        }
        return requests.get(self.url, params=params)


class SJ_API(BaseAPI):

    def __init__(self):
        self.url = 'https://api.superjob.ru/2.0/vacancies'

    def get_vacancies(self, keyword, page=1):
        params = {
            'keywords': keyword,
            'page': page
        }
        headers = eval(os.environ['headers'])
        return requests.get(self.url, headers=headers, params=params)
