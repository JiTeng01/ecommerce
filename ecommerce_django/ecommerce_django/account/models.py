from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db.models import Count, Q
from django.contrib.auth.models import Group
from toolbox.db.models import (models, BaseModel, BaseModelQuerySet, BaseModelManager, TokenMixin, OTPMixin,
                               AWSImageModel)
from toolbox.db.address.models import AbstractAddressModel
from toolbox.utilities.datetime import (today, now, stringify_date, stringify_datetime, DateFormatter,
                                        DateTimeFormatter)
from toolbox.utilities.encodes import base64_encode, base64_decode, json_encode, json_decode, generate_unique_code
from toolbox.utilities.os import os
from epanel.constants.account import Status, Gender, UserRole


class UserQuerySet(BaseModelQuerySet):

    def username(self, username):
        return self.filter(username=username)

    def username_icontains(self, username):
        return self.filter(username__icontains=username)

    def phone_number(self, phone_number):
        return self.filter(phone_number=phone_number)

    def token(self, token):
        return self.filter(token=token)


class UserManager(BaseUserManager, BaseModelManager):

    def get_queryset(self):
        return UserQuerySet(self.model, self._db)
    
    def get_one_by_token(self, token):
        return self.get_all().token(token).first()

    def get_one_by_username(self, username, exclude=None):
        queryset = self.get_all().username(username)

        if isinstance(exclude, User):
            queryset = queryset.exclude(pk=exclude.id)

        return queryset.first()

    def create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, BaseModel, PermissionsMixin, TokenMixin):

    username = models.CharField(max_length=40, unique=True, default=None, verbose_name="Username")
    email = models.EmailField(blank=True, null=True, verbose_name="Email")

    objects = UserManager()

    USERNAME_FIELD = "username"

    class Meta:
        db_table = "account_user"
        indexes = [models.Index(fields=["id"])]
        permissions = (('view_users', 'Can view users'), ('is_user', 'Is a normal user'),
                       ('is_admin', 'Is a system admin'))

    @property
    def can_login(self):
        return True if self.status == Status.ACTIVATE else False

    @property
    def group(self):
        return self.groups.all().first()

    @property
    def is_locked(self):
        return self.status == Status.LOCKED

    @property
    def encrypted_username(self):
        return base64_encode(self.username)

    def stringify_last_login(self, datetime_format=DateTimeFormatter.DEFAULT_FORMAT):
        return stringify_datetime(self.last_login, datetime_format=datetime_format) if self.last_login else "N.A."

    def set_inactivate(self):
        self.status = Status.INACTIVATE
        self.save()


class AccountQuerySet(BaseModelQuerySet):

    def user(self, user):
        return self.filter(user=user)

    def username_icontains(self, username):
        return self.filter(user__username__icontains=username)

    def full_name(self, full_name):
        return self.filter(full_name=full_name)

    def full_name_icontains(self, full_name):
        return self.filter(full_name__icontains=full_name)

    def email(self, email, exclude=False):
        if exclude:
            return self.exclude(user__email=email)
        return self.filter(user__email=email)

    def email_icontains(self, email):
        return self.filter(user__email__icontains=email)

    def phone_number_icontains(self, phone_number):
        return self.filter(phone_number__icontains=phone_number)

    def is_superuser(self, is_superuser):
        return self.filter(user__is_superuser=is_superuser)

    def group(self, group):
        return self.filter(user__groups__in=group)

    def sign_up_date(self, sign_up_date):
        return self.filter(created_on__date=sign_up_date)

    def dob_gte(self, dob_gte):
        return self.filter(dob__gte=dob_gte)

    def dob_lte(self, dob_lte):
        return self.filter(dob__lte=dob_lte)

    def unique_code(self, unique_code):
        return self.filter(unique_code=unique_code)

    def gender(self, gender):
        return self.filter(gender=gender)

    def last_login_date(self, last_login_date):
        return self.filter(user__last_login__date=last_login_date)

    def last_login_date_lte(self, last_login_date):
        return self.filter(user__last_login__date__lte=last_login_date)

    def last_login_date_gte(self, last_login_date):
        return self.filter(user__last_login__date__gte=last_login_date)

    def postal_code_icontains(self, postal_code):
        return self.filter(postal_code__icontains=postal_code)


class AccountManager(BaseModelManager):

    def get_queryset(self):
        return AccountQuerySet(self.model, using=self._db)

    def get_one_by_user(self, user):
        return self.get_all().user(user).first()

    def get_one_by_email(self, email):
        return self.get_all().email(email).first()

    def get_all_members(self):
        group = Group.objects.all().filter(name=UserRole.USER_NAME)
        return self.get_all().is_superuser(False).is_deleted(False).group(group)


class Account(BaseModel):

    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=250, blank=True, null=True, verbose_name="First Name")
    last_name = models.CharField(max_length=250, blank=True, null=True, verbose_name="Last Name")
    full_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Full Name")
    gender = models.CharField(max_length=1, choices=Gender.CHOICES, blank=True, null=True, default=None,
                              verbose_name="Gender")
    dob = models.DateField(blank=True, null=True, verbose_name="Date of Birth")
    phone_number = models.CharField(max_length=20, default=None, verbose_name="Phone number")

    objects = AccountManager()

    class Meta:
        db_table = "account_account"
        indexes = [models.Index(fields=["id"]), models.Index(fields=["user"])]
        permissions = (("add_admin", "Can add admin"), ("edit_admin", "Can edit admin"),
                       ("manage_admin_permission", "Can manage admin permission"),
                       ("change_admin_password", "Can change admin password"),
                       ("delete_member", "Can delete member account"),
                       ("change_member_subscription", "Can change member subscription"))

    def get_age(self):
        if self.dob:
            diff_years = today().year - self.dob.year
            return diff_years + 1 if today().month > self.dob.month else diff_years
        return 0

    @property
    def is_agreed_terms(self):
        return self.terms



    @property
    def total_tokens(self):
        return self.free_tokens + self.premium_tokens


    def stringify_dob(self, date_format=DateFormatter.DEFAULT_FORMATIV):
        return stringify_date(self.dob, date_format=date_format) if self.dob else ""

    def get_meta_data(self, field_name=None):
        try:
            meta_data = {}
            if self.meta_data:
                meta_data = json_decode(self.meta_data)

            if field_name:
                return meta_data.get(field_name, [])
            return meta_data
        except Exception as e:
            return {} if not field_name else []

    def set_meta_data(self, field_name, value):
        try:
            meta_data = self.get_meta_data()
            meta_data[field_name] = value
            self.meta_data = json_encode(meta_data)
            self.save()
        except Exception as e:
            return None




