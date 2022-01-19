import requests


class Scraper:
    def __init__(self, link):
        self.link = link

    def get_page_content(self):
        return requests.get(self.link).content
