from utils import get_hh_data, create_database, save_data_to_database
from config import config


def main():
    api_key = 'https://api.hh.ru/employers/'
    employers_ids = [
        '2324020',  # "Точка"
        # '5760737',  # "Нетвижн"
        # '9035637',  # "DataGo"
        # '4010751',  # "KVINT"
        # '238161',   # "СИГМА"
        # '3183420',  # "Digital Reputation"
        # '2970204',  # "ОТУС"
        # '32570',    #  "ICL"
        # '1740',     # "Яндекс"
        # '67611'    # "Тензор"
    ]
    params = config()

    data = get_hh_data(api_key, employers_ids)
    print(data)
    # create_database('HeadHunter', params)
    # save_data_to_database(data, 'HeadHunter', params)


if __name__ == '__main__':
    main()