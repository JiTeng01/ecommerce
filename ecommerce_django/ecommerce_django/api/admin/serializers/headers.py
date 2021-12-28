from toolbox.api.serializers.headers import BaseTableHeader


class AdminHeader:

    sn = BaseTableHeader("S/N", "sn")
    username = BaseTableHeader("Username", "username")
    full_name = BaseTableHeader("Full Name", "fullname")
    email = BaseTableHeader("Email", "email")
    contact_number = BaseTableHeader("Phone Number", "phonenumber")
    action = BaseTableHeader("Action", "action")

    class Meta:
        fields = ["sn", "username", "full_name", "email", "contact_number", "action"]

    def get_headers(self):
        return [getattr(self, field).__dict__ for field in self.Meta.fields]
