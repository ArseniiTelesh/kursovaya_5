from abc import ABC, abstractmethod
import os
import json


class Saver(ABC):

    @abstractmethod
    def add_vacancy(self):
        pass

    @abstractmethod
    def get_vacancies_by_salary(self):
        pass

    @abstractmethod
    def delete_vacancy(self):
        pass


class JSONSaver(Saver):

    def __init__(self, file_path):
        self.data_file = file_path

    @staticmethod
    def _make_file(filename):
        if not os.path.exists(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))

        if not os.path.exists(filename):
            with open(filename, 'w') as file:
                file.write(json.dumps([]))

    @staticmethod
    def _open_file(filename):
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)

    @property
    def data_file(self):
        return self.__data_file

    @data_file.setter
    def data_file(self, new_data):
        self.__data_file = new_data
        self._make_file(self.__data_file)

    def add_vacancy(self, data):
        file_data = self._open_file(self.__data_file)
        file_data.append(data)

        with open(self.__data_file, 'w', encoding='utf-8') as file:
            json.dump(file_data, file, indent=4, ensure_ascii=False)

    def get_vacancies_by_salary(self, salary):
        file_data = self._open_file(self.__data_file)

        if not salary:
            return file_data

        result = []
        for item in file_data:
            if all(item.get(key) == value for key, value in salary.items()):
                result.append(item)

        return result

    def delete_vacancy(self, vacancy):
        file_data = self._open_file(self.__data_file)

        if not vacancy:
            return file_data

        result = []
        for item in file_data:
            if not all(item.get(key) == value for key, value in vacancy.items()):
                result.append(item)

        with open(self.__data_file, 'w', encoding='utf-8') as file:
            json.dump(result, file)
