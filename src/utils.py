from typing import Any
import requests
import json


def get_hh_data(hh_api_key: str, employers_ids: list[str]) -> list[dict[str, Any]]:
    """Получение данных о компаниях и их вакансиях при помощи API HeadHunter"""

    data = []
    for employer_id in employers_ids:
        employer_data = requests.get(hh_api_key+employer_id).content.decode()
        employer_data_json = json.loads(employer_data)

        emp_vacancies_data = requests.get(employer_data_json['vacancies_url']).content.decode()
        emp_vacancies_data_json = json.loads(emp_vacancies_data)

        data.append({
            'channel': employer_data_json,
            'videos': emp_vacancies_data_json
            })

    return data


def create_database():
    pass


def save_data_to_database():
    pass
