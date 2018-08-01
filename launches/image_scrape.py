"""
Builds a url from a rocket name and scrapes google image search.
Returns the src of the first thumbnail (normally around 120x150px).
Search options are for portrait images with a non-commercial usage licence.

Identified options in query string parameters:
tbm=isch    image search
tbs=iar:t   tall orientation
tbs=sur:f   labeled for non-commercial use
"""
from bs4 import BeautifulSoup
import requests


def scrape_img_src(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.text)
    return soup.img['src']


def build_url(rocket_name):
    url = f"https://www.google.co.uk/search?q={rocket_name}+rocket+launch&tbs=iar:t,sur:f&tbm=isch"
    return url
