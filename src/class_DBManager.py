import psycopg2


class DBManager:

    def __init__(self, db_params):
        """
        Инициализация объекта DBManager.
        """
        self.connection = None
        self.db_params = db_params

    def connect(self):
        """
        Устанавливает соединение с БД.
        """
        try:
            self.connection = psycopg2.connect(**self.db_params)
            print("Подключение к БД успешно установлено.")
        except (psycopg2.Error, Exception) as e:
            print(f"Ошибка при подключении к БД: {e}")

    def close_connection(self):
        """
        Закрывает соединение с БД.
        """
        if self.connection:
            self.connection.close()
            print("Соединение с БД закрыто.")

    def execute_query(self, query):
        """
        Выполняет SQL-запрос к БД и возвращает результат запроса.
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchall()
        except (psycopg2.Error, Exception) as e:
            print(f"Ошибка при выполнении запроса: {e}")
            return None

    def get_companies_and_vacancies_count(self):
        """
        Получает список всех компаний и количество вакансий у каждой компании.
        """
        query = """SELECT employer_name, COUNT(vacancy_id) as vacancy_count
                FROM employer LEFT JOIN vacancies ON employer.employer_id = vacancies.employer_id
                GROUP BY employer_name"""
        result = self.execute_query(query)
        return result

    def get_all_vacancies(self):
        """
        Получает список всех вакансий с указанием названия компании, названия вакансии, зарплаты и ссылки на вакансию.
        """
        query = """SELECT employer.employer_name, vacancy_name, salary, vacancy_url
                FROM vacancies LEFT JOIN employer ON vacancies.employer_id = employer.employer_id"""
        result = self.execute_query(query)
        return result

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям."""
        query = "SELECT AVG(salary) as average_salary FROM vacancies"
        result = self.execute_query(query)
        return result[0][0] if result and result[0][0] else 0

    def get_vacancies_with_higher_salary(self):
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        """
        avg_salary = self.get_avg_salary()
        query = f"""SELECT employer.employer_name, vacancy_name, salary, vacancy_url
                FROM vacancies LEFT JOIN employer ON vacancies.employer_id = employer.employer_id
                WHERE salary > {avg_salary}"""
        result = self.execute_query(query)
        return result

    def get_vacancies_with_keyword(self):
        """
        Получает список всех вакансий, в названии которых содержатся переданные в метод слова.
        """
        keyword = input('Введите слово, по которому хотите найти вакансии: ')
        query = f"""SELECT employer.employer_name, vacancy_name, salary, vacancy_url
                FROM vacancies LEFT JOIN employer ON vacancies.employer_id = employer.employer_id
                WHERE LOWER(vacancy_name) LIKE LOWER('%{keyword}%')"""
        result = self.execute_query(query)
        return result

