class Passenger:
    count_id = 0

    def __init__(self, first_name, last_name, nric, phone_no, email, seat_no, flight_no, gender, health_declaration , pcr_test , pre_book, remarks):
        Passenger.count_id += 1
        self.__passenger_id = Passenger.count_id
        self.__first_name = first_name
        self.__last_name = last_name
        self.__nric = nric
        self.__phone_no = phone_no
        self.__email = email
        self.__flight_no = flight_no
        self.__seat_no = seat_no
        self.__gender = gender
        self.__health_declaration = health_declaration
        self.__pcr_test = pcr_test
        self.__pre_book = pre_book
        self.__remarks = remarks

    def get_passenger_id(self):
        return self.__passenger_id

    def get_first_name(self):
        return self.__first_name

    def get_last_name(self):
        return self.__last_name

    def get_nric(self):
        return self.__nric

    def get_phone_no(self):
        return self.__phone_no

    def get_email(self):
        return self.__email

    def get_flight_no(self):
        return self.__flight_no

    def get_seat_no(self):
        return self.__seat_no

    def get_gender(self):
        return self.__gender

    def get_health_declaration(self):
        return self.__health_declaration

    def get_pcr_test(self):
        return self.__pcr_test

    def get_pre_book(self):
        return self.__pre_book

    def get_remarks(self):
        return self.__remarks

    def set_passenger_id(self, passenger_id):
        self.__passenger_id = passenger_id

    def set_first_name(self, first_name):
        self.__first_name = first_name

    def set_last_name(self, last_name):
        self.__last_name = last_name

    def set_nric(self, nric):
        self.__nric = nric

    def set_phone_no(self, phone_no):
        self.__phone_no = phone_no

    def set_email(self, email ):
        self.__email = email

    def set_flight_no(self, flight_no):
        self.__flight_no = flight_no

    def set_seat_no(self, seat_no):
        self.__seat_no = seat_no

    def set_gender(self, gender):
        self.__gender = gender

    def set_health_declaration(self, health_declaration):
        self.__health_declaration = health_declaration

    def set_pcr_test(self, pcr_test):
        self.__pcr_test = pcr_test

    def set_pre_book(self, pre_book):
        self.__pre_book = pre_book

    def set_remarks(self, remarks):
        self.__remarks = remarks

