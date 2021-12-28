from django import forms
from django.contrib.auth.models import Group, Permission
from django.contrib.auth import get_user_model
from django.http import request
from toolbox.api.constants.message import ADD_SUCCESS, ADD_ERROR, SAVE_SUCCESS, SAVE_ERROR, PASSWORD_SUCCESS, PASSWORD_ERROR
from toolbox.utilities.encodes import base64_decode
from toolbox.api.serializers import Pagination
from account.models import Account, Status, User
from epanel.constants.account import UserRole
from epanel.constants.admin import AdminPermission
from toolbox.utilities.encodes import json_decode


class AdminListForm(forms.Form):

    page = forms.IntegerField(required=False)
    username = forms.CharField(required=False)
    full_name = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(AdminListForm, self).__init__(*args, **kwargs)
        self.pagination = None

    def clean(self):
        super(AdminListForm, self).clean()
        self.username = self.cleaned_data.get('username', "")
        self.full_name = self.cleaned_data.get("full_name", "")
        self.page = self.cleaned_data.get("page", 1)

    def get_items(self):
        group = Group.objects.all().filter(name__in=[UserRole.ADMIN_NAME, UserRole.LOGISTICS_NAME])

        object_list = Account.objects.all().is_deleted(False)

        object_list = object_list.exclude_by_pk(self.request.user.account.id).group(group)
        if self.username:
            object_list = object_list.username_icontains(self.username)

        if self.full_name:
            object_list = object_list.full_name_icontains(self.full_name)

        object_list = object_list.order_by("id")
        self.pagination = Pagination(object_list)

        return self.pagination.get_items(self.page)

    def get_pagination(self):
        return dict(num_pages=self.pagination.num_pages)
    
    def get_permissions(self):
        if self.request.user.is_superuser:
            return dict(add_admin=True)

        return dict(add_admin=self.request.user.has_perm(AdminPermission.ADD_ADMIN))

    def get_roles(self):
        return UserRole.SELECT_LIST[:2]

    @staticmethod
    def get_all():
        group = Group.objects.all().filter(name=UserRole.ADMIN_NAME)
        return Account.objects.all().is_superuser(False).is_deleted(False).group(group)


class AdminCreateForm(forms.Form):

    model = get_user_model()

    username = forms.CharField(required=True)
    password = forms.CharField(required=True)
    repeat_password = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    full_name = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)
    role = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(AdminCreateForm, self).__init__(*args, **kwargs)

    def clean_username(self):
        self.username = self.cleaned_data.get("username")
        if isinstance(self.model.objects.get_one_by_username(self.username), self.model):
            self.add_error("username", "Username already in used")

    def clean_role(self):
        self.role = self.cleaned_data.get('role')
        if self.role and self.role not in UserRole.CODE_LIST:
            self.add_error("role", "Role is required")
        return self.role

    def clean(self):
        super(AdminCreateForm, self).clean()
        self.email = self.cleaned_data.get("email")
        self.full_name = self.cleaned_data.get("full_name")
        self.phone_number = self.cleaned_data.get("phone_number")
        self.password = base64_decode(self.cleaned_data.get("password"))
        self.repeat_password = base64_decode(self.cleaned_data.get("repeat_password"))

    def is_valid(self):
        valid = super(AdminCreateForm, self).is_valid()
        if self.password != self.repeat_password:
            self.add_error("repeat_password", "Password does not match")
            return False
        return valid

    def save(self):
        role_name = UserRole.get_name(self.role)
        user = self.model.objects.create_user(self.username, self.email, self.password)
        Account.objects.create(user=user, full_name=self.full_name, phone_number=self.phone_number)
        group = Group.objects.all().filter(name=role_name).first()
        user.groups.add(group)

    def get_success_message(self):
        return ADD_SUCCESS

    def get_error_message(self):
        return ADD_ERROR

class AdminUpdateForm(forms.Form):
    pk = forms.ModelChoiceField(queryset=AdminListForm.get_all(), required=True)
    email = forms.EmailField(required=True)
    full_name = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)
    permissions = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(AdminUpdateForm, self).__init__(*args, **kwargs)
        self._instance = None

    def clean_pk(self):
        self._instance = self.cleaned_data.get("pk")
    
    def clean_permissions(self):
        self.permissions = self.cleaned_data.get("permissions", "")
        try:
            self.permissions = json_decode(self.permissions)
        except:
            self.permissions = []

        if len(self.permissions) > 0:
            self.permissions = Permission.objects.filter(pk__in=self.permissions)
        return self.permissions

    def clean(self):
        super(AdminUpdateForm, self).clean()
        self.email = self.cleaned_data.get("email")
        self.full_name = self.cleaned_data.get("full_name")
        self.phone_number = self.cleaned_data.get("phone_number")

    def save(self):
        self._instance.user.email = self.email
        self._instance.user.save()
        self._instance.nric_name, self._instance.phone_number = self.full_name, self.phone_number
        self._instance.user.user_permissions.clear()
        if len(self.permissions) > 0:
            for permission in self.permissions:
                user_permission = Permission.objects.filter(id=permission.id).first()
                user_permission = self._instance.user.user_permissions.add(permission)

        self._instance.save()
        return self._instance

    def get_success_message(self):
        return SAVE_SUCCESS

    def get_error_message(self):
        return SAVE_ERROR

class AdminDeleteForm(forms.Form):
    instance = forms.ModelChoiceField(queryset=User.objects.get_all(), required=True)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(AdminDeleteForm, self).__init__(*args, **kwargs)
        self.error_message = ""

    def clean(self):
        super(AdminDeleteForm, self).clean()
        self.instance = self.cleaned_data.get("instance")

    def is_valid(self):
        valid = super(AdminDeleteForm, self).is_valid()

        if not self.request.user.is_superuser or not self.request.user.has_perm(AdminPermission.EDIT_ADMIN):
            self.error_message = "You do not have permission to delete admin"
            return False
        return valid

    def delete(self):
        user = self.instance
        
        if isinstance(user, User):
            user.delete()

    def get_success_message(self):
        return ""

    def get_error_message(self):
        return self.error_message
