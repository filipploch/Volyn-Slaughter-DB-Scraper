from scraper import Scraper
from bs4 import BeautifulSoup


class VictimLinkGetter(Scraper):
    def __init__(self, link):
        super().__init__(link)

    def get_all_links(self):
        return BeautifulSoup(self.get_page_content(), 'html.parser').find('div', class_='okno').find_all('a')
