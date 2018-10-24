import requests as rq
from bs4 import BeautifulSoup


class Scraper:

    """ scrapes text from <p> tags"""

    def __init__(self, url):
        self.url = url

    def scrape(self):

        """ scrapes text from <p> tags"""
        try:
            docu = rq.get(self.url, timeout=5)
            soup = BeautifulSoup(docu.text, 'lxml')
            return [block.text.strip() for block in soup.find_all('p')]
        except rq.RequestException as err:
            return str(err)


