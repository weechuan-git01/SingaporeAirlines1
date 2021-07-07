class Employer:
    count_id = 0

    def __init__(self,company_name, company_location, industry, establishment_date, company_logo, email, contact, facebook, instagram, social_media, website, remarks):
        Employer.count_id += 1
        self.__employer_id = Employer.count_id
        self.__login_id = ''
        self.__password = ''
        self.__company_name = company_name
        self.__company_location = company_location
        self.__industry = industry
        self.__establishment_date = establishment_date
        self.__company_logo = company_logo
        self.__email = email
        self.__contact = contact
        self.__facebook = facebook
        self.__instagram = instagram
        self.__social_media = social_media
        self.__website = website
        self.__remarks = remarks
        self.__no_of_listings = 0

    def get_employer_id(self):
        return self.__employer_id

    def get_login_id(self):
        return self.__login_id

    def get_password(self):
        return self.__password

    def get_company_name(self):
        return self.__company_name

    def get_company_location(self):
        return self.__company_location

    def get_industry(self):
        return self.__industry

    def get_establishment_date(self):
        return self.__establishment_date

    def get_company_logo(self):
        return self.__company_logo

    def get_email(self):
        return self.__email

    def get_contact(self):
        return self.__contact

    def get_facebook(self):
        return self.__facebook

    def get_instagram(self):
        return self.__instagram

    def get_social_media(self):
        return self.__social_media

    def get_website(self):
        return self.__website

    def get_remarks(self):
        return self.__remarks

    def get_no_of_listings(self):
        return self.__no_of_listings

    def set_employer_id(self, employer_id):
        self.__employer_id = employer_id

    def set_login_id(self, login_id):
        self.__login_id = login_id

    def set_password(self, password):
        self.__password = password

    def set_company_name(self, company_name):
        self.__company_name = company_name

    def set_company_location(self, company_location):
        self.__company_location = company_location

    def set_industry(self, industry):
        self.__industry = industry

    def set_establishment_date(self, establishment_date):
        self.__establishment_date = establishment_date

    def set_company_logo(self, company_logo):
        self.__company_logo = company_logo

    def set_email(self, email):
        self.__email = email

    def set_contact(self, contact):
        self.__contact = contact

    def set_facebook(self, facebook):
        self.__facebook = facebook

    def set_instagram(self, instagram):
        self.__instagram = instagram

    def set_social_media(self, social_media):
        self.__social_media = social_media

    def set_website(self, website):
        self.__website = website

    def set_remarks(self, remarks):
        self.__remarks = remarks

    def set_no_of_listings(self, no_of_listings):
        self.__no_of_listings = no_of_listings