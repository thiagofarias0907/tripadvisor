from bs4 import BeautifulSoup

from studio import Studio

import re

class Parser:

    def __init__(self, content: str):
        self.parsed_page = BeautifulSoup(content, features="html.parser")

    def get_list_elements(self) -> [BeautifulSoup]:
        list_elements = self.parsed_page.select('section[data-automation="WebPresentation_SingleFlexCardSection"]')
        return list_elements

    def get_studios(self) -> [Studio]:
        studios = [self.parse_element(element) for element in self.get_list_elements()]
        return list(studios)

    def parse_element(self, element: BeautifulSoup):
        order, name = self.parse_name(element)
        category, location = self.parse_category_and_location(element)

        studio = Studio(
            order=order,
            name=name,
            url=self.parse_url(element),
            n_reviews=self.parse_number_of_reviews(element),
            score=self.parse_score(element),
            category=category,
            location=location
        )

        return studio

    def parse_name(self, element: BeautifulSoup) -> (int,str):
        inner_text = element.select_one("header a").text

        ## Todo: raise of an exception or log in case of failures here (at every function, actually)
        groups = re.search("(\\d+)\\.\\s+(.*)", inner_text).groups()
        order = int(groups[0].strip())
        name = groups[1].strip()

        return order, name

    def parse_url(self, element: BeautifulSoup) -> str:
        return element.select_one("header a").get('href').strip()

    def parse_number_of_reviews(self, element: BeautifulSoup) -> int:
        score_text = element.select_one("header a:nth-of-type(2) span").text
        return int(score_text.replace(',',''))

    def parse_score(self, element: BeautifulSoup) -> float:
        score_text = element.select_one("header a:nth-of-type(2) title").text
        score_value = score_text.split(" of ")[0].strip()
        score = float(score_value)
        return score

    def parse_category_and_location(self, element: BeautifulSoup) -> (str, str):
        info_element = element.select_one('header + div > div > div > div')
        category_element = info_element.select_one("div")
        category = category_element.text.strip()

        # todo: must be tested against other result pages and null cases
        location_element = info_element.select("div:nth-of-type(4) > div")
        location = None
        if location_element is not None:
            if len(location_element) > 1:
                location = location_element[0].text.strip()

        return category, location