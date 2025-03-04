import asyncio
import unittest
from unittest.mock import patch

from app import api
from fastapi.testclient import TestClient

import os

from studio import Studio
from scraper import Scraper


client = TestClient(api)

def side_effect():
    return [
            Studio(
                order=i,
                name=str(i),
                url=str(i),
                n_reviews=i,
                score=i,
                location=str(i),
                category=str(i),
            ) for i in range(0, 10)
        ]


class AppTestCase(unittest.TestCase):

    def test_base_route(self):
        with patch.object(Scraper, 'extract_companies', return_value=side_effect()) as mock_method:
            response = client.get("/companies")
            self.assertEqual(200, response.status_code)
            self.assertEqual("http://testserver/companies",response.url)

            mock_method.assert_called()

    def test_filter_path(self):
        with patch.object(Scraper, 'extract_companies', return_value=side_effect()) as mock_method:
            response = client.get("/companies/France/1")
            self.assertEqual(200, response.status_code)
            self.assertEqual("http://testserver/companies/France/1",response.url)

            mock_method.assert_called()


if __name__ == '__main__':
    unittest.main()
