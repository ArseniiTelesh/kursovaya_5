from abc import ABC, abstractmethod
import requests
import os


class BaseAPI(ABC):

    @abstractmethod
    def get_request(self):
        pass


class HH_API(BaseAPI):

    def __init__(self, keyword, page=0):
        self.url = 'https://api.hh.ru/vacancies'
        self.params = {
            'text': keyword,
            'page': page
        }

    def get_request(self):
        return requests.get(self.url, params=self.params)


class SJ_API(BaseAPI):

    def __init__(self, keyword, page=1):
        self.url = 'https://api.superjob.ru/2.0/vacancies'
        self.params = {
            'keywords': keyword,
            'page': page
        }

    def get_request(self):
        headers = eval(os.environ['headers'])
        return requests.get(self.url, headers=headers, params=self.params)
