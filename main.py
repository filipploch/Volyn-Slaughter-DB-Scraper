import json
from time import sleep
from bs4 import BeautifulSoup
import requests
from sqlite3 import connect, Error


class DatabaseSetup:
    def __init__(self):
        self.db_file = 'Volyn-Slaughter.db'

    def create_connection(self):
        conn = None
        try:
            conn = connect(self.db_file)
        except Error as e:
            print(e)
        return conn

    def add_record_to_db(self, conn, data):
        query = '''
                INSERT INTO IPNdata
                (link, name, death_date, province, district, community, place_of_death, death_info,
                number_of_victims, nationality, place_of_living, congregation, source, attachment, also_check)
                VALUES
                (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)            
        '''
        cur = conn.cursor()
        cur.execute(query, [json.loads(data)['link'], json.loads(data)['name'], json.loads(data)['death_date'],
                            json.loads(data)['province'], json.loads(data)['district'], json.loads(data)['community'],
                            json.loads(data)['place_of_death'], json.loads(data)['death_info'],
                            json.loads(data)['number_of_victims'], json.loads(data)['nationality'],
                            json.loads(data)['place_of_living'], json.loads(data)['congregation'],
                            json.loads(data)['source'], json.loads(data)['attachment'], json.loads(data)['also_check'],
                            ])
        conn.commit()


class Scraper:
    def __init__(self, link):
        self.link = link

    def get_page_content(self):
        return requests.get(self.link).content


class VictimLinkGetter(Scraper):
    def __init__(self, link):
        super().__init__(link)

    def get_all_links(self):
        return BeautifulSoup(self.get_page_content(), 'html.parser').find('div', class_='okno').find_all('a')


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


class Victim:
    def __init__(self, data_dict):
        self.link = data_dict['link']
        self.name = data_dict['Nazwisko i imię / Zbrodnia']
        self.death_date = data_dict['Data śmierci / Data zbrodni']
        self.province = data_dict['Województwo']
        self.district = data_dict['Powiat']
        self.community = data_dict['Gmina:']
        self.place_of_death = data_dict['Miejsce śmierci / Miejsce zbrodni']
        self.death_info = data_dict['Informacje / Okoliczności śmierci']
        self.number_of_victims = data_dict['Liczba ofiar']
        self.nationality = data_dict['Narodowość / Przynależność etniczna']
        self.place_of_living = data_dict['Miejsce zamieszkania']
        self.congregation = data_dict['Parafia (wg. zamieszkania)']
        self.source = data_dict['Źródło']
        self.attachment = data_dict['Opisy załączników, linki zewnętrzne']
        self.also_check = data_dict['Zobacz również']

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          indent=4, ensure_ascii=False)


if __name__ == '__main__':
    conn = DatabaseSetup().create_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS IPNData
             (id INTEGER NOT NULL PRIMARY KEY, link, name, death_date, province, district, community, place_of_death, death_info,
                number_of_victims, nationality, place_of_living, congregation, source, attachment, also_check)''')
    for site in range(2835):
        if not site:
            site_link = 'https://zbrodniawolynska.pl/zw1/form/247,Baza-Ofiar-Zbrodni-Wolynskiej.html'
        else:
            site_link = f'https://zbrodniawolynska.pl/zw1/form/247,Baza-Ofiar-Zbrodni-Wolynskiej.html?page={site}'
        links = VictimLinkGetter(site_link).get_all_links()
        for link in links:

            with conn:
                link = f'https://zbrodniawolynska.pl{link["href"]}'
                victim = Victim(VictimDataScraper(link).get_data())
                try:
                    DatabaseSetup().add_record_to_db(conn, victim.to_json())
                    sleep(0.01)
                except Error as e:
                    print(e)



