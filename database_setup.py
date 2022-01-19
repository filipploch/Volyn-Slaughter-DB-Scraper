from sqlite3 import connect, Error
import json


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