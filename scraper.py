from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from parser import Parser



# Todo: Could use selenium to get these codes directly (however, it might be unecessary do this at every request considering scale)
countries = {
    "United_States": "g191",
    "France": "g187070",
    "Spain": "g187427",
}

class Scraper:

    def __init__(self, country_name: str = "United_States", page_number=1, driver=None):
        self.country = country_name
        self.page_number = page_number
        self.driver = driver

    def extract_companies(self):
        url = self.create_url()
        self.driver.get(url)

        try:
            element = WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-automation='LeftRailMain'"))
            )

            if element is not None:
                parser = Parser(element.get_attribute('innerHTML'))
                save_file(create_id(url),element.get_attribute('innerHTML'))
                return parser.get_studios()

        except Exception as ex:
            print(f"extract_companies failure: {ex}")

        finally:
            self.driver.quit()

    def create_url(self) -> str:
        country = f"-{self.country}"
        country_code = countries[self.country]
        page_part = "" if self.page_number == 1 else f"-oa{30 * (self.page_number - 1)}"
        return f'https://www.tripadvisor.com/Attractions-{country_code}-Activities-c40-t129,260{page_part}{country}.html'


def save_file(id: str, content: str):
    try:
        file_name = f'data/{id}.html'

        import os
        if not os.path.exists('data'):
            os.mkdir('data')

        with open(file_name, 'w', encoding="utf8") as file:
            file.write(content)
    except Exception as ex:
        print(f"saving file failure: {ex.__str__()}")


def create_id(url: str):
    return url.split('.com/')[1].split('.html')[0]