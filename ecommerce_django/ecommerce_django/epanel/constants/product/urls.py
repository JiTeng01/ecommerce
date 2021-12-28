from toolbox.utilities.urls import BaseURL

class ProductAPIURL(BaseURL):

    URL_LIST = "api:product:list"
    URL_DETAILS = "api:product:details"

    @classmethod
    def get_list_url(cls):
        return cls._get_url(cls.URL_LIST, is_redirect=False)

    @classmethod
    def get_details_url(cls, args=None):
        return cls._get_url(cls.URL_DETAILS, args=args, is_redirect=False)