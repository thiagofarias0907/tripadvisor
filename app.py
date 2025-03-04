from typing import List, Annotated

import undetected_chromedriver as uc

import uvicorn
from fastapi import FastAPI, Path

from parser import Parser
from scraper import Scraper
from studio import Studio

import os
import yaml
from yaml import CLoader


# Local Config File
config = None
with open(os.path.dirname(__file__) + '/config.yml', 'r', encoding='utf8') as file:
    config = yaml.load(file, Loader=CLoader)

description = """
TripAdvisor.com simple web scraper that extracts from the filtered result page the "Attraction's" name, detailed url link, rating, number of reviews, category and location if exposed

## List the companies / attractions listed 
You can list and filter the products from a single page by:

* By three countries: "United_States", "France", "Spain"
* Score Rating greater than a specific value.
* Number of reviews greater than a specific value.
* Filter by category. 

"""

api = FastAPI(
    title='TripAdvisor Result Page Scraper',
    description=description
)


@api.get('/companies', response_model=List[Studio])
def get_companies():
    scraper = Scraper(driver=driver)
    result = scraper.extract_companies()
    return result


@api.get('/companies/{country}/{page_number}',
         response_model=List[Studio],
         description="Filter by country (United_States, France or Spain) and page")
def get_companies_by_country(country: Annotated[str, Path(title="Options: United_States, France or Spain")],
                        page_number: int | None):
    scraper = Scraper(country_name=country, page_number=page_number, driver=driver)
    result = scraper.extract_companies()
    return result


# Opening Selenium controlled Browser - Using Undetected Chrome give better results than regular webdriver.Firefox()
# If you are having problem with setting this driver, check their docs or replace this bya a regular Selenium browser
# Caution: As in every web scraping project be aware of the risks of blocking your own IP.
#          Use a vpn or add proxy controller and argument in the options bellow
options = uc.ChromeOptions()
options.add_argument(f"--window-size=1920,1080")
options.add_argument(
    f'--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument("--disable-extensions")
options.add_argument("--proxy-server='direct://'")
options.add_argument("--proxy-bypass-list=*")
options.add_argument('--ignore-certificate-errors')
options.add_argument("--password-store=basic")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-extensions")
options.add_argument("--enable-automation")
options.add_argument("--disable-browser-side-navigation")
options.add_argument("--disable-web-security")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-infobars")
options.add_argument("--disable-gpu")
options.add_argument("--disable-setuid-sandbox")
options.add_argument("--disable-software-rasterizer")
options.add_argument(f"--user-data-dir={config['chrome_profile_path']}")

driver = uc.Chrome(executable_path=f'{config['chrome_path']}', options=options, version_main= 132)

if __name__ == "__main__":
    uvicorn.run(api, host="localhost", port=8080)