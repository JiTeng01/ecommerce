from django.db import models
from django.conf import settings
from toolbox.utilities.os import has_file, delete_file
from toolbox.utilities.encodes import json_encode, json_decode
from toolbox.utilities.image import resize_image, resize_image_aws
from toolbox.utilities.strings import generate_random_string
from toolbox.utilities.datetime import timezone, timedelta, stringify_datetime, DateTimeFormatter, datetime


class BaseModelQuerySet(models.QuerySet):

    def pk(self, pk):
        return self.filter(pk=pk)

    def pks(self, pks):
        return self.filter(pk__in=pks)

    def pk_gt(self, pk):
        return self.filter(pk__gt=pk)

    def pk_gte(self, pk):
        return self.filter(pk__gte=pk)

    def pk_lte(self, pk):
        return self.filter(pk__lte=pk)

    def is_deleted(self, is_deleted):
        return self.filter(is_deleted=is_deleted)

    def exclude_by_pk(self, pk):
        return self.exclude(pk=pk)

    def exclude_by_pks(self, pks):
        return self.exclude(pk__in=pks)

    def created_on_range(self, start_time, end_time):
        return self.filter(created_on__range=(start_time, end_time))

    def created_date(self, created_date):
        return self.filter(created_on__date=created_date)

    def created_date_range(self, start_date, end_date):
        return self.filter(created_on__date__range=(start_date, end_date))

    def created_date_lte(self, date):
        return self.filter(created_on__date__lte=date)

    def created_date_gte(self, date):
        return self.filter(created_on__date__gte=date)

    def created_on_week_day(self, week_day):
        return self.filter(created_on__week_day=week_day)

    def updated_date_range(self, start_date, end_date):
        return self.filter(updated_on__date__range=(start_date, end_date))

    def updated_date_lte(self, date):
        return self.filter(updated_on__date__lte=date)

    def updated_date_gte(self, date):
        return self.filter(updated_on__date__gte=date)


class BaseModelManager(models.Manager):

    def get_all(self, is_deleted=False):
        queryset = self.get_queryset().all()

        if is_deleted in [True, False]:
            queryset = queryset.is_deleted(is_deleted)

        return queryset

    def get_one_by_pk(self, pk):
        return self.filter(pk=pk).is_deleted(False).first()


class BaseModel(models.Model):

    created_on = models.DateTimeField(default=timezone.now, editable=False)
    updated_on = models.DateTimeField(default=timezone.now)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def soft_delete(self):
        self.is_deleted = True
        self.save()
        return self

    def save(self, *args, **kwargs):
        if self.id:
            self.updated_on = timezone.now()
        return super(BaseModel, self).save(*args, **kwargs)

    def stringify_created(self, datetime_format=DateTimeFormatter.DEFAULT_FORMAT, default_message=""):
        if not self.created_on:
            return default_message
        return stringify_datetime(self.created_on, datetime_format=datetime_format, timezone=settings.TIME_ZONE)

    def stringify_updated(self, datetime_format=DateTimeFormatter.DEFAULT_FORMAT, default_message=""):
        if not self.updated_on:
            return default_message
        return stringify_datetime(self.updated_on, datetime_format=datetime_format, timezone=settings.TIME_ZONE)


class KeyValueModelQuerySet(BaseModelQuerySet):

    def key(self, key):
        return self.filter(key=key)

    def key_icontains(self, key):
        return self.filter(key__icontains=key)

    def value(self, value):
        return self.filter(value=value)

    def value_icontains(self, value):
        return self.filter(value__icontains=value)

    def exclude_by_key(self, key):
        return self.exclude(key=key)

    def exclude_by_value(self, value):
        return self.exclude(value=value)


class KeyValueModelManager(BaseModelManager):

    def get_queryset(self):
        return KeyValueModelQuerySet(self.model, using=self._db)

    def get_one_by_key(self, key):
        return self.get_queryset().is_deleted(False).key(key=key).first()


class KeyValueModel(BaseModel):

    key = models.CharField(max_length=50, unique=True)
    value = models.CharField(max_length=255)

    objects = KeyValueModelManager()

    class Meta:
        abstract = True

    def __str__(self):
        return "%s - %s" % (self.key, self.value)

    def __unicode__(self):
        return "%s - %s" % (self.key, self.value)

    def value_decode(self, decode_type="json", default_value=None):
        try:
            if decode_type == "json" and self.value:
                return json_decode(self.value)
            return default_value
        except:
            return default_value

    @classmethod
    def value_encode(cls, encoded_value, decode_type="json"):
        try:
            if decode_type == "json":
                return json_encode(encoded_value)
            return None
        except Exception as e:
            return None


class ImageModel(models.Model):

    class Meta:
        abstract = True

    def create_thumbnail(self):
        if self.image and has_file(self.image.path):
            destination_url = self.image.path.replace('.', '_thumbnail.')
            if resize_image(self.image.path, destination_url=destination_url, width=700):
                self.thumbnail = self.image.name.replace('.', '_thumbnail.')
                self.save()

    def delete_images(self):
        if self.image and has_file(self.image.path):
            delete_file(self.image.path)
        if self.thumbnail and has_file(self.thumbnail.path):
            delete_file(self.thumbnail.path)

    def get_upload_path(self):
        return ""

    def get_image_url(self):
        return self.image.url if self.image else ""

    def get_thumbnail_url(self):
        return self.thumbnail.url if self.thumbnail else ""


class AWSImageModel(ImageModel):

    class Meta:
        abstract = True

    def delete_images(self):
        if self.image is not None:
            self.image.delete(save=False)

        if self.thumbnail is not None:
            self.thumbnail.delete(save=False)

    def create_thumbnail(self):
        self.thumbnail = resize_image_aws(self.image)
        self.thumbnail.name = self.image.name.replace('.', '_thumbnail.')
        self.save()


class TokenMixin(models.Model):
    """
    Add the fields and methods necessary to support the token authentication method
    using the ModelBackend.
    """
    token = models.CharField(max_length=100, blank=True, null=True)
    expiry_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True

    def get_token(self, length=10, valid_duration=120):
        """
        generate a random strings token without saving
        """

        minutes = valid_duration if not settings.AUTH_VALID_DURATION else settings.AUTH_VALID_DURATION
        self.token = "".join(generate_random_string(length))
        self.expiry_time = timezone.now() + timedelta(minutes=minutes)

    def generate_token(self, length=10, valid_duration=120):
        self.get_token(length=length, valid_duration=valid_duration)
        self.save(update_fields=['token', 'expiry_time'])

    def destroy_token(self):
        self.token, self.expiry_time = None, None
        self.save(update_fields=['token', 'expiry_time'])

    @property
    def is_expired(self):
        if self.token is None or self.expiry_time is None:
            return True

        return self.expiry_time <= datetime.now()

    def extend_expiry(self, valid_duration=120):
        if self.expiry_time:
            self.expiry_time += timedelta(minutes=valid_duration)
        self.save()
        return self

    def stringify_expiry_time(self, datetime_format=DateTimeFormatter.DEFAULT_FORMAT, default_message=""):
        if not self.expiry_time:
            return default_message
        return stringify_datetime(self.expiry_time, datetime_format=datetime_format)


class OTPMixin(models.Model):
    """
    Add the fields and methods necessary to support the token authentication method
    using the ModelBackend.
    """
    otp_code = models.CharField(max_length=100, blank=True, null=True)
    otp_expiry_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True

    def get_otp_code(self, length=6, valid_duration=5):
        """
        generate a random strings token without saving
        """

        minutes = valid_duration
        if hasattr(settings, "AUTH_VALID_OTP_DURATION"):
            minutes = getattr(settings, "AUTH_VALID_OTP_DURATION")

        self.otp_code = "".join(generate_random_string(length, mode="digits"))
        self.otp_expiry_time = timezone.now() + timedelta(minutes=minutes)

    def generate_otp_code(self, length=6, valid_duration=5):
        self.get_otp_code(length=length, valid_duration=valid_duration)
        self.save(update_fields=['otp_code', 'otp_expiry_time'])

    def destroy_otp_code(self):
        self.otp_code, self.otp_expiry_time = None, None
        self.save(update_fields=['otp_code', 'otp_expiry_time'])

    @property
    def is_otp_expired(self):
        if self.otp_code is None or self.otp_expiry_time is None:
            return True

        return self.otp_expiry_time <= datetime.now()

    def stringify_otp_expiry_time(self, datetime_format=DateTimeFormatter.DEFAULT_FORMAT, default_message=""):
        if not self.otp_expiry_time:
            return default_message
        return stringify_datetime(self.otp_expiry_time, datetime_format=datetime_format)
