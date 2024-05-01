import re

salary_pattern = r'\d{1,3}(?:\s\d{3})*(?:\.\d+)?' # паттерн нахождения зарплаты
currency_pattern = re.compile(r'\s(₽|\$|€)')

def salary_parser(salary: str) -> int:

    matches = re.findall(salary_pattern, salary)

    if salary.startswith("от") and len(matches) == 1:
        return [int(matches[0].replace(" ", "")), None]
    elif salary.startswith("до") and len(matches) == 1:
        return [None, int(matches[0].replace(" ", ""))]
    elif len(matches) == 0:
        return [None, None]
    else:
        return [int(matches[0].replace(" ", "")),int(matches[1].replace(" ", ""))]


def currency_parser(salary: str) -> str:
    currency = currency_pattern.search(salary)
    return currency.group(1)