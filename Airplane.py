class Airplane:
    count_id = 0

    def __init__(self, tail_number, operation_status, model, airline, hanger, remarks, last_maintenance, in_charge, date_diff):
        Airplane.count_id += 1
        self.__airplane_id = Airplane.count_id
        self.__tail_number = tail_number
        self.__operation_status = operation_status
        self.__model = model
        self.__airline = airline
        self.__hanger = hanger
        self.__remarks = remarks
        self.__last_maintenance = last_maintenance
        self.__in_charge = in_charge
        self.__date_diff = date_diff

    def get_airplane_id(self):
        return self.__airplane_id

    def get_tail_number(self):
        return self.__tail_number

    def get_operation_status(self):
        return self.__operation_status

    def get_model(self):
        return self.__model

    def get_airline(self):
        return self.__airline

    def get_hanger(self):
        return self.__hanger

    def get_remarks(self):
        return self.__remarks

    def get_last_maintenance(self):
        return self.__last_maintenance

    def get_in_charge(self):
        return self.__in_charge

    def get_date_diff(self):
        return self.__date_diff

    def set_airplane_id(self, airplane_id):
        self.__airplane_id = airplane_id

    def set_tail_number(self, tail_number):
        self.__tail_number = tail_number

    def set_operation_status(self, operation_status):
        self.__operation_status = operation_status

    def set_model(self, model):
        self.__model = model

    def set_airline(self, airline):
        self.__airline = airline

    def set_hanger(self, hanger):
        self.__hanger = hanger

    def set_remarks(self, remarks):
        self.__remarks = remarks

    def set_last_maintenance(self, last_maintenance):
        self.__last_maintenance = last_maintenance

    def set_in_charge(self, in_charge):
        self.__in_charge = in_charge

    def set_date_diff(self, date_diff):
        self.__date_diff = date_diff
