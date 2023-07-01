from APIs_classes import HH_API, SJ_API
from funcs import sorting, get_top, get_hh_vacancies, get_sj_vacancies


def main():
    while True:
        keyword: str = input('Введите слово, по которому хотите искать вакансии: ')

        hh = HH_API()
        sj = SJ_API()

        hh_saver = hh.get_json_saver('parsed_data/hh_vacancies.json')
        sj_saver = sj.get_json_saver('parsed_data/sj_vacancies.json')

        for page in range(1):

            hh_vacancies = hh.get_vacancies(keyword).json()['items']
            for vacancy in hh_vacancies:
                hh_saver.add_vacancy(vacancy)

            sj_vacancies = sj.get_vacancies(keyword).json()['objects']
            for vacancy in sj_vacancies:
                sj_saver.add_vacancy(vacancy)

        while True:

            command = input('Введите команду ("sort" или "top"): ')

            if command == 'sort':
                hh_vacancies = get_hh_vacancies(hh_saver)
                sj_vacancies = get_sj_vacancies(sj_saver)

                sorted_vacancies = sorting(hh_vacancies + sj_vacancies)

                for vacancy in sorted_vacancies:
                    print(vacancy)

            elif command == 'top':

                hh_vacancies = get_hh_vacancies(hh_saver)
                sj_vacancies = get_sj_vacancies(sj_saver)

                all_vacancies = hh_vacancies+sj_vacancies

                top_count = int(input('Введите число, сколько вакансий хотите увидеть: '))

                top_vacancies = get_top(all_vacancies, top_count)

                for vacancy in top_vacancies:
                    print(vacancy)

            else:
                print('Такой команды не существует, попробуйте еще раз. ')

            continue_searching = input("Хотите провести езщё один анализ вакансий? ('yes'/'no'): ")

            if continue_searching == 'no':
                break

        new_search = input("Хотите поискать другие вакансии? ('yes'/'no'): ")

        if new_search == 'no':
            break


if __name__ == '__main__':
    main()