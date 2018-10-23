import requests as rq
from bs4 import BeautifulSoup


class Scraper:

    """ scrapes text from <p> tags"""

    def __init__(self, url):
        self.url = url

    def scrape(self):
        docu = rq.get(self.url)
        soup = BeautifulSoup(docu.text, 'lxml')
        return [block.text.strip() for block in soup.find_all('p')]


