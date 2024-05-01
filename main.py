from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from configparser import ConfigParser
import datetime
import pytz
from typing import Generator, Optional

from parsers.dateparser import created_at_parser, published_at_parser
from parsers.salaryparser import salary_parser, currency_parser


config = ConfigParser()
config.read('config.ini')

query = config['DEFAULT']['QueryString']
timezone = config['DEFAULT']['TimeZone']
base_url = config['DEFAULT']['BaseURL']


class Vacancy:
    def __init__(self) -> None:
        self.VACANCIES = []
        self.LINKS = set()
        self.driver = webdriver.Firefox()
        self.driver.get(base_url)


    @property
    def vacancies(self):
        return self.VACANCIES
    
    @vacancies.setter
    def vacancies(self, value):
        self.VACANCIES.append(value)

    @property
    def links(self):
        return self.LINKS
    
    @links.setter
    def links(self, value):
        self.LINKS.add(value)

    def _get_vacancies(self) -> None:

        '''Получаем список вакансий в браузере'''

        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//input[@name="keywords"]'))
        )

        inputs = self.driver.find_element(By.XPATH, '//input[@name="keywords"]')
        inputs.send_keys(query, Keys.ENTER)

    def _list_vacancies(self) -> None:

        '''Формируем списки ссылок и вакансий'''

        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "f-test-search-result-item"))
        )

        jobs = self.driver.find_elements(By.CLASS_NAME, 'f-test-search-result-item')

        for job in jobs[1:]:
            childs = job.find_elements(By.XPATH, "./*")
            for child in childs:
                if len(child.text)!=0:
                    hrefs = child.find_elements(By.XPATH, "//a[starts-with(@href, '/vakansii/') and string-length(substring-after(@href, '/vakansii/')) > 0]")
                    for href in hrefs[1:]:
                        self.links = href.get_attribute("href")
                    self.vacancies = child.text

    def build_vacancies(self) -> Generator[Optional[dict], None, None]:
        
        '''Создаем генератор из собранных данных'''

        LINKS = list(self.links)

        for id, vacancy in enumerate(self.vacancies):
            splitted_str = vacancy.split('\n')

            data = {}
            try:
                for key, value in enumerate(splitted_str):
                    match key:
                        case 0:
                            date = published_at_parser(value, timezone)
                            data["published_at"] = date
                            data["created_at"] = created_at_parser(timezone)
                        case 1:
                            data["position"] = value
                        case 2:
                            data["salary_from"], data["salary_to"] = salary_parser(value)
                            data["currency"] = currency_parser(value)
                        case 4:
                            data["city"] = value
                        case 5:
                            data["description"] = "".join(i for i in splitted_str[key:len(splitted_str)-2])
                            data["link"] = LINKS[id]

            except Exception as e:
                yield None
            
            else:
                yield data

            finally:
                data = {}

    def _exit(self):
        return self.driver.quit()




    
if __name__ == "__main__":
    from validator import VacancyValidator
    from pydantic import ValidationError
    from tinydb import TinyDB, Query

    vac = Vacancy()

    vac._get_vacancies()
    vac._list_vacancies()
    vac._exit()

    db = TinyDB('vacancies.json')

    for v in vac.build_vacancies():
        if v is not None:
            try:
                vv = VacancyValidator(**v)
                db.insert(vv.model_dump())
            except Exception as e:
                print(e)
                print("Возможно попалась реклама, или нет...")

    db.close()
    





