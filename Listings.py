class Listings:
    count_no = 0

    def __init__(self, job_title, no_of_hires, job_description, job_requirements, position_required):
        Listings.count_no += 1
        self.__listing_no = Listings.count_no
        self.__company = ''
        self.__job_title = job_title
        self.__no_of_hires = no_of_hires
        self.__job_description = job_description
        self.__job_requirements = job_requirements
        self.__position_required = position_required
        self.__match = ''
        self.__no_of_matches = 0

    def get_listing_no(self):
        return self.__listing_no

    def get_company(self):
        return self.__company

    def get_job_title(self):
        return self.__job_title

    def get_no_of_hires(self):
        return self.__no_of_hires

    def get_job_description(self):
        return self.__job_description

    def get_job_requirements(self):
        return self.__job_requirements

    def get_position_required(self):
        return self.__position_required

    def get_match(self):
        return self.__match

    def get_no_of_matches(self):
        return self.__no_of_matches

    def set_listing_no(self, listing_no):
        self.__listing_no = listing_no

    def set_company(self, company):
        self.__company = company

    def set_job_title(self, job_title):
        self.__job_title = job_title

    def set_no_of_hires(self, no_of_hires):
        self.__no_of_hires = no_of_hires

    def set_job_description(self, job_description):
        self.__job_description = job_description

    def set_job_requirements(self, job_requirements):
        self.__job_requirements = job_requirements

    def set_position_required(self, position_required):
        self.__position_required = position_required

    def set_match(self, match):
        self.__match = match

    def set_no_of_matches(self, no_of_matches):
        self.__no_of_matches = no_of_matches