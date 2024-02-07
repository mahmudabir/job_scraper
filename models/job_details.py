class JobDetails:
    def __init__(
        self,
        job_title=None,
        location=None,
        company_name=None,
        # search_parameter=None,
        website=None,
        email=None,
        phone=None,
    ):
        self.job_title = job_title
        self.location = location
        self.company_name = company_name
        # self.search_parameter = search_parameter
        self.website = website
        self.email = email
        self.phone = phone

    @property
    def __keys__(self):
        key_list = list(self.__dict__.keys())
        return key_list
