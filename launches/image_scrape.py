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
import logging
import requests


def scrape_img(rocket_name):
    """Google image search scraping.
    Extracts the first image from a page of google image search results and returns a
    response object
    """
    url = f"https://www.google.co.uk/search?q={rocket_name}+rocket+launch&tbs=iar:t,sur:f&tbm=isch"
    image_search_page = requests.get(url)
    image_search_soup = BeautifulSoup(image_search_page.text, features='html.parser')
    img_url = image_search_soup.img['src']
    return requests.get(img_url)


def save_img(binary, filepath):
    """
    Writes an image binary to a local file.

    :binary: content of the response object containing the binary of the image
    :filepath: full local filepath where the file should be written
    """
    try:
        with open(filepath, 'wb') as f:
            f.write(binary)
            logging.info(f'Written image file: {filepath}')
    except FileNotFoundError as e:
        # likely due to an error with the filepath and probably not going to work on
        # another attempt
        raise e


def get_rocket_img(rocket_name, filepath):
    """Wrapper for the scraping and local write of a rocket image"""
    image = scrape_img(rocket_name)
    save_img(image.content, filepath)
