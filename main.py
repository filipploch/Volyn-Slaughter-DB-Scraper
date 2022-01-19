from time import sleep
from sqlite3 import Error
from database_setup import DatabaseSetup
from victim_link_getter import VictimLinkGetter
from victim_data_scraper import VictimDataScraper
from victim import Victim
from varia import LINK

def main():
    conn = DatabaseSetup().create_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS IPNData
             (id INTEGER NOT NULL PRIMARY KEY, link, name, death_date, province, district, community, place_of_death, death_info,
                number_of_victims, nationality, place_of_living, congregation, source, attachment, also_check)''')
    for site in range(2835):
        if not site:
            site_link = LINK
        else:
            site_link = f'{LINK}?page={site}'
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

if __name__ == '__main__':
    main()