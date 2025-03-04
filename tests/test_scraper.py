import unittest

from scraper import Scraper

class ScraperTestCase(unittest.TestCase):
    def test_url_building(self):
        scraper = Scraper("Spain", 1)
        self.assertEqual("https://www.tripadvisor.com/Attractions-g187427-Activities-c40-t129,260-Spain.html",
                         scraper.create_url())
        scraper = Scraper("United_States")
        self.assertEqual("https://www.tripadvisor.com/Attractions-g191-Activities-c40-t129,260-United_States.html",
                         scraper.create_url())
        scraper = Scraper("France", 2)
        self.assertEqual("https://www.tripadvisor.com/Attractions-g187070-Activities-c40-t129,260-oa30-France.html",
                         scraper.create_url())


if __name__ == '__main__':
    unittest.main()
