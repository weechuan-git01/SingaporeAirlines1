class Ticket:
    count_id = 0

    def __init__(self, departure_country, arrival_country, return_date, flight_class, adults, children):
        Ticket.count_id += 1
        self.__ticket_id = Ticket.count_id
        self.__type = ''
        self.__departure_country = departure_country
        self.__arrival_country = arrival_country
        self.__return_date = return_date
        self.__flight_class = flight_class
        self.__adults = adults
        self.__children = children
        self.__number_of_rebooked = 0
        self.__number_of_flying = 0
        self.__number_of_postpones = 0

    def get_ticket_id(self):
        return self.__ticket_id

    def get_type(self):
        return self.__type

    def get_departure_country(self):
        return self.__departure_country

    def get_arrival_country(self):
        return self.__arrival_country

    def get_return_date(self):
        return self.__return_date

    def get_flight_class(self):
        return self.__flight_class

    def get_adults(self):
        return self.__adults

    def get_children(self):
        return self.__children

    def set_ticket_id(self, ticket_id):
        self.__ticket_id = ticket_id

    def set_type(self, type):
        self.__type = type

    def set_departure_country(self, departure_country):
        self.__departure_country = departure_country

    def set_arrival_country(self, arrival_country):
        self.__arrival_country = arrival_country

    def set_return_date(self, return_date):
        self.__return_date = return_date

    def set_flight_class(self, flight_class):
        self.__flight_class = flight_class

    def set_adults(self, adults):
        self.__adults = adults

    def set_children(self, children):
        self.__children = children

    def get_number_of_rebooked(self):
        return self.__number_of_rebooked

    def get_number_of_postpones(self):
        return self.__number_of_postpones

    def get_number_of_flying(self):
        return self.__number_of_flying

    def set_number_of_rebooked(self, number_of_rebooked):
        self.__number_of_rebooked = number_of_rebooked

    def set_number_of_postpones(self, number_of_postpones):
        self.__number_of_postpones = number_of_postpones

    def set_number_of_flying(self, number_of_flying):
        self.__number_of_flying = number_of_flying
