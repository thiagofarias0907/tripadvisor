# Tripadvisor Web Scraping

## About
TripAdvisor.com simple web scraper that extracts from the filtered result page the "Attraction's" name, detailed url link, rating, number of reviews, category and location if exposed.


## Technologies
 - BeautifulSoup
 - Selenium
 - FastApi
 - unittest


## How to Run it
 - Create a venv
 - Run the pip install -f and install the libraries using the `requirements.txt` file
 - Run the api `uvicorn app.main:app --reload` 

And your app will be running on http://localhost:8000/

### Docs:
Access http://localhost:8000/docs to use the built-in interface.

### How to run the test files
 - `python -m unittest discover Tests`