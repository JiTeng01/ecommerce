from toolbox.utilities.urls import BaseURL

class AdminAPIURL(BaseURL):

    URL_LIST = "api:admin:list"
    URL_DETAILS = "api:admin:details"
    URL_PASSWORD = "api:admin:password"

    @classmethod
    def get_list_url(cls):
        return cls._get_url(cls.URL_LIST, is_redirect=False)

    @classmethod
    def get_details_url(cls, args=None):
        return cls._get_url(cls.URL_DETAILS, args=args, is_redirect=False)

    @classmethod
    def get_password_url(cls, args=None):
        return cls._get_url(cls.URL_PASSWORD, args=args, is_redirect=False)


class AdminPermissionAPIURL(BaseURL):

    URL_LIST = "api:epanel:admin:permission:list"

    @classmethod
    def get_list_url(cls, args=None):
        return cls._get_url(cls.URL_LIST, args=args, is_redirect=False)