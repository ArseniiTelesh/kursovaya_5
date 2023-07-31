from utils import get_hh_data, create_database, save_data_to_database
from config import config
from class_DBManager import DBManager
import os


def main():
    api_key = 'https://api.hh.ru/employers/'
    employers_ids = [
        '2324020',  # "Точка"
        '3188177',  # "АТРАКС ТРЕЙД"
        '9035637',  # "DataGo"
        '951200',   # "Компания Дилявер"
        '5819349',  # "Miles&Miles"
        '5658700',  # "Люди для Вас"
        '736233',   # "МДО"
        '5179890',  # "Enjoypro"
        '2515455',  # "24Н Софт"
        '67611'     # "Тензор"
    ]
    params = config()

    data = get_hh_data(api_key, employers_ids)

    create_database('headhunter', params)
    save_data_to_database(data, 'headhunter', params)

    # Прописать свои данные в переменные окружения
    db_host = os.getenv('host')
    db_database = os.getenv('database')
    db_password = os.getenv('password')
    db_port = os.getenv('port')
    hh_db_params = {'host': db_host, 'database': db_database, 'password': db_password, 'port': db_port}

    manager = DBManager(hh_db_params)
    manager.connect()

    print(manager.get_companies_and_vacancies_count())
    print(manager.get_all_vacancies())
    print(manager.get_avg_salary())
    print(manager.get_vacancies_with_higher_salary())
    print(manager.get_vacancies_with_keyword())


if __name__ == '__main__':
    main()
