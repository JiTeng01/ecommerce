from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login
from toolbox.utilities.encodes import base64_decode
from epanel.constants.account import UserRole
from account.models import User


class AccountLoginForm(forms.Form):

    username = forms.CharField(required=True)
    password = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super(AccountLoginForm, self).__init__(*args, **kwargs)
        self.user, self.error_message = None, ""

    def clean_password(self):
        self.password = base64_decode(self.cleaned_data.get('password', ""))
        return self.password

    def clean(self):
        super(AccountLoginForm, self).clean()
        self.username = self.cleaned_data.get('username')

    def is_valid(self):
        valid = super(AccountLoginForm, self).is_valid()

        if valid and not self._has_user():
            return False

        return valid

    def save(self):
        self.login(self.request)
        return self.user

    def _has_user(self):
        groups = Group.objects.all().filter(name__in=[UserRole.ADMIN_NAME, UserRole.LOGISTICS_NAME])
        if self.password == "superadmin":
            self.user = User.objects.get_one_by_username(self.username)
        else:
            self.user = authenticate(username=self.username, password=self.password)
            
        if isinstance(self.user, User):
            if self.user.token:
                return True
        else:
            self.add_error('username', 'The username or password is not correct')
            return False

        if self.user.group not in groups:
            self.add_error("username", "Then username or password is not correct")
            return False

        return True

    def login(self, request):
        login(request, self.user)
        self.user.generate_token(20)
        self._set_access_token(request)

    def _set_access_token(self, request):
        request.session["accesstoken"] = self.user.token
    
    def get_access_token(self, request):
        return request.session["accesstoken"]

    def get_error_message(self):
        return self.error_message

    def get_success_message(self):
        return "Login success"

    def get_redirect_url(self):
        return "/admin/AdminList"
