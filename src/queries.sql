
--Получает список всех компаний и количество вакансий у каждой компании.

SELECT employer_name, COUNT(vacancy_id) as vacancy_count
FROM employer LEFT JOIN vacancies ON employer.employer_id = vacancies.employer_id
GROUP BY employer_name


--Получает список всех вакансий с указанием названия компании, названия вакансии, зарплаты и ссылки на вакансию.

SELECT employer.employer_name, vacancy_name, salary, vacancy_url
FROM vacancies LEFT JOIN employer ON vacancies.employer_id = employer.employer_id


--Получает среднюю зарплату по вакансиям

SELECT AVG(salary) as average_salary FROM vacancies


--Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.

SELECT employer.employer_name, vacancy_name, salary, vacancy_url
FROM vacancies LEFT JOIN employer ON vacancies.employer_id = employer.employer_id
WHERE salary > AVG(salary)


--Получает список всех вакансий, в названии которых содержатся переданные в метод слова.

SELECT employer.employer_name, vacancy_name, salary, vacancy_url
FROM vacancies LEFT JOIN employer ON vacancies.employer_id = employer.employer_id
WHERE LOWER(vacancy_name) LIKE LOWER('%{keyword}%')
