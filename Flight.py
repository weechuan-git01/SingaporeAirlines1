class Flight:
    count_id = 0

    def __init__(self, flight_number, departure_country, arrival_country, departure_date, fly, flight_type):
        Flight.count_id += 1
        self.__flight_id = Flight.count_id
        self.__flight_number = flight_number
        self.__departure_country = departure_country
        self.__arrival_country = arrival_country
        self.__departure_date = departure_date
        self.__fly = fly
        self.__flight_type = flight_type

    def get_flight_id(self):
        return self.__flight_id

    def get_flight_number(self):
        return self.__flight_number

    def get_departure_country(self):
        return self.__departure_country

    def get_arrival_country(self):
        return self.__arrival_country

    def get_departure_date(self):
        return self.__departure_date

    def get_fly(self):
        return self.__fly

    def get_flight_type(self):
        return self.__flight_type

    def set_flight_id(self, flight_id):
        self.__flight_id = flight_id

    def set_flight_number(self, flight_number):
        self.__flight_number = flight_number

    def set_departure_country(self, departure_country):
        self.__departure_country = departure_country

    def set_arrival_country(self, arrival_country):
        self.__arrival_country = arrival_country

    def set_departure_date(self, departure_date):
        self.__departure_date = departure_date

    def set_fly(self,fly):
        self.__fly = fly

    def set_flight_type(self, flight_type):
        self.__flight_type= flight_type