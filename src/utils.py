from typing import Any
import requests
import json
import psycopg2


def get_hh_data(hh_api_key: str, employers_ids: list[str]) -> list[dict[str, Any]]:
    """Получение данных о компаниях и их вакансиях при помощи API HeadHunter"""

    data = []
    for employer_id in employers_ids:
        employer_data = requests.get(hh_api_key+employer_id).content.decode()
        employer_data_json = json.loads(employer_data)

        emp_vacancies_data = requests.get(employer_data_json['vacancies_url']).content.decode()
        emp_vacancies_data_json = json.loads(emp_vacancies_data)

        data.append({
            'employer': employer_data_json,
            'vacancies': emp_vacancies_data_json
            })

    return data


def create_database(database_name: str, params: dict):
    """Создание базы данных и таблиц для сохранения данных о компаниях и вакансиях."""

    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE {database_name}")
    cur.execute(f"CREATE DATABASE {database_name}")

    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE employer (
                employer_id SERIAL PRIMARY KEY,
                employer_name VARCHAR(255) NOT NULL,
                description TEXT,
                area VARCHAR,
                site_url TEXT
            )
        """)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE vacancies (
                vacancy_id SERIAL PRIMARY KEY,
                employer_id INTEGER REFERENCES employer(employer_id),
                vacancy_name VARCHAR NOT NULL,
                published_at DATE,
                salary INTEGER,
                vacancy_url TEXT
            )
        """)
    conn.commit()
    conn.close()


def save_data_to_database(data: list[dict[str, Any]], database_name: str, params: dict):
    """Сохранение данных о компаниях и вакансиях в базу данных."""

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        for company in data:
            employer_data = company['employer']

            cur.execute(
                """
                INSERT INTO employer (employer_name, description, area, site_url)
                VALUES (%s, %s, %s, %s)
                RETURNING employer_id
                """,
                (employer_data['name'], employer_data['description'], employer_data['area']['name'],
                 employer_data['site_url'])
            )
            employer_id = cur.fetchone()[0]
            vacancies_data = company['vacancies']['items']
            for vacancy in vacancies_data:
                cur.execute(
                    """
                    INSERT INTO vacancies (employer_id, vacancy_name, published_at, salary, vacancy_url)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING vacancy_id
                    """,
                    (employer_id, vacancy['name'], vacancy['published_at'],
                     vacancy['salary']['from'], vacancy['alternate_url'])
                )
            cur.execute(
            """UPDATE vacancies
            SET salary = CASE WHEN salary IS NULL THEN 0 ELSE salary END
            """
            )
    conn.commit()
    conn.close()
