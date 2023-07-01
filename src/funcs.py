from job_classes import Vacancy, HHVacancy, SJVacancy


def sorting(vacancies: list[Vacancy]):
    return sorted(vacancies, reverse=True)


def get_top(vacancies: list[Vacancy], top_count: int):
    return sorted(vacancies, reverse=True)[:top_count]


def get_hh_vacancies(saver):
    vacanies = [
        HHVacancy(
            title=vacancy['name'],
            link=vacancy['alternate_url'],
            description=vacancy['snippet'],
            salary=vacancy['salary']['from'] if vacancy.get('salary') else '0'
        )
        for vacancy in saver.get_vacancies_by_salary()
    ]
    return vacanies


def get_sl_vacancies(saver):
    vacanies = [
        SJVacancy(
            title=vacancy['profession'],
            link=vacancy['link'],
            description=vacancy['candidat'],
            salary=vacancy['payment_from']
        )
        for vacancy in saver.get_vacancies_by_salary()
    ]
    return vacanies
