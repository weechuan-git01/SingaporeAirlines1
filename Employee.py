class Employee:
    count_id = 0

    def __init__(self, first_name, last_name, birthdate, gender, nationality, photo,  role, employment_status, job_start_date, level_of_education, major, school, graduation_date, address, mobile_contact, home_contact, email, remarks):
        Employee.count_id += 1
        self.__employee_id = Employee.count_id
        self.__login_id = ''
        self.__password = ''
        self.__first_name = first_name
        self.__last_name = last_name
        self.__age = 0
        self.__birthdate = birthdate
        self.__gender = gender
        self.__nationality = nationality
        self.__photo = photo

        self.__role = role
        self.__employment_status = employment_status
        self.__job_start_date = job_start_date
        self.__job_end_date = ''
        self.__year_of_service = 0

        self.__level_of_education = level_of_education
        self.__major = major
        self.__school = school
        self.__graduation_date = graduation_date

        self.__address = address
        self.__mobile_contact = mobile_contact
        self.__home_contact = home_contact
        self.__email = email
        self.__remarks = remarks

        self.__timestamp = ''
        self.__task = ''
        self.__match = ''
        self.__no_of_matches = 0

    def set_employee_id(self, employee_id):
        self.__employee_id = employee_id

    def set_login_id(self, login_id):
        self.__login_id = login_id

    def set_password(self, password):
        self.__password = password

    def set_first_name(self, first_name):
        self.__first_name = first_name

    def set_last_name(self, last_name):
        self.__last_name = last_name

    def set_age(self, age):
        self.__age = age

    def set_birthdate(self, birthdate):
        self.__birthdate = birthdate

    def set_gender(self, gender):
        self.__gender = gender

    def set_nationality(self, nationality):
        self.__nationality = nationality

    def set_photo(self, photo):
        self.__photo = photo

    def set_role(self, role):
        self.__role = role

    def set_employment_status(self, employment_status):
        self.__employment_status = employment_status

    def set_job_start_date(self, job_start_date):
        self.__job_start_date = job_start_date

    def set_job_end_date(self, job_end_date):
        self.__job_end_date = job_end_date

    def set_year_of_service(self, year_of_service):
        self.__year_of_service = year_of_service


    def set_level_of_education(self, level_of_education):
        self.__level_of_education = level_of_education

    def set_major(self, major):
        self.__major = major

    def set_school(self, school):
        self.__school = school

    def set_graduation_date(self, graduation_date):
        self.__graduation_date = graduation_date


    def set_address(self, address):
        self.__address = address

    def set_mobile_contact(self, mobile_contact):
        self.__mobile_contact = mobile_contact

    def set_home_contact(self, home_contact):
        self.__home_contact = home_contact

    def set_email(self, email):
        self.__email = email

    def set_remarks(self, remarks):
        self.__remarks = remarks


    def set_timestamp(self, timestamp):
        self.__timestamp = timestamp

    def set_task(self, task):
        self.__task = task

    def set_match(self, match):
        self.__match = match

    def set_no_of_matches(self, no_of_matches):
        self.__no_of_matches = no_of_matches


    def get_employee_id(self):
        return self.__employee_id

    def get_login_id(self):
        return self.__login_id

    def get_password(self):
        return self.__password

    def get_first_name(self):
        return self.__first_name

    def get_last_name(self):
        return self.__last_name

    def get_age(self):
        return self.__age

    def get_birthdate(self):
        return self.__birthdate

    def get_gender(self):
        return self.__gender

    def get_nationality(self):
        return self.__nationality

    def get_photo(self):
        return self.__photo

    def get_role(self):
        return self.__role

    def get_employment_status(self):
        return self.__employment_status

    def get_job_start_date(self):
        return self.__job_start_date

    def get_job_end_date(self):
        return self.__job_end_date

    def get_year_of_service(self):
        return self.__year_of_service


    def get_level_of_education(self):
        return self.__level_of_education

    def get_major(self):
        return self.__major

    def get_school(self):
        return self.__school

    def get_graduation_date(self):
        return self.__graduation_date

    def get_address(self):
        return self.__address

    def get_mobile_contact(self):
        return self.__mobile_contact

    def get_home_contact(self):
        return self.__home_contact

    def get_email(self):
        return self.__email

    def get_remarks(self):
        return self.__remarks


    def get_timestamp(self):
        return self.__timestamp

    def get_task(self):
        return self.__task

    def get_match(self):
        return self.__match

    def get_no_of_matches(self):
        return self.__no_of_matches
