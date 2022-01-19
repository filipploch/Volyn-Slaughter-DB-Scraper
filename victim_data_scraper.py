from scraper import Scraper
from bs4 import BeautifulSoup


class VictimDataScraper(Scraper):
    def __init__(self, link):
        super().__init__(link)

    def get_data(self):
        divs_ins = BeautifulSoup(self.get_page_content(), 'html.parser').find_all(name='div', class_='ins')
        data_dict = {'link': self.link}
        for div_ins in divs_ins:
            label = BeautifulSoup(str(div_ins), 'html.parser').find('div', class_='label').text.replace("\n", "")
            text = BeautifulSoup(str(div_ins), 'html.parser').find('div', class_='form_text').text.replace("\n", "")
            data_dict.update({label: text})
        return data_dict