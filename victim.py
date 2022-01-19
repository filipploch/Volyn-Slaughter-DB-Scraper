import json


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
