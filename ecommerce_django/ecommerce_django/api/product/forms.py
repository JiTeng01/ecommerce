from django import forms
from toolbox.api.serializers import Pagination
from django.core.files.base import ContentFile
from toolbox.utilities.encodes import base64_decode_raw
from toolbox.utilities.datetime import now, stringify_datetime, DateTimeFormatter
from product.models import Product
from toolbox.api.constants.message import (ADD_SUCCESS, ADD_ERROR, SAVE_SUCCESS, SAVE_ERROR, DELETE_EXIST_ERROR,
                                           DELETE_ERROR, DELETE_SUCCESS)


class ProductListForm(forms.Form):

    page = forms.IntegerField(required=True)
    code = forms.CharField(required=False)
    name = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(ProductListForm, self).__init__(*args, **kwargs)
        self.pagination = None

    def clean(self):
        super(ProductListForm, self).clean()
        self.code = self.cleaned_data.get('code', "")
        self.name = self.cleaned_data.get('name', "")
        self.page = self.cleaned_data.get('page', "")

    def get_items(self):
        object_list = Product.objects.get_all()

        if self.code:
            object_list = object_list.code_icontain(self.code)

        if self.name:
            object_list = object_list.name_icontains(self.name)

        object_list = object_list.order_by("code")

        self.pagination = Pagination(object_list)

        return self.pagination.get_items(self.page)

    def get_pagination(self):
        return dict(num_pages=self.pagination.num_pages)

    @staticmethod
    def get_all():
        return Product.objects.get_all().order_by("code")


class ProductCreateForm(forms.Form):
    code = forms.CharField(required=True)
    name = forms.CharField(required=True)
    price = forms.FloatField(required=True)
    description = forms.CharField(required=True)
    discount = forms.IntegerField(required=False)
    image = forms.CharField(required=True)
    image_link = forms.URLField(required=False)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(ProductCreateForm, self).__init__(*args, **kwargs)
        self.code, self.name, self.price, self.description, self.discount, self.image_format, self.image_binary = None, None, None, None, None, None, None
    
    def clean_image(self):
        image = self.cleaned_data.get('image', "")
        self.image_format, self.image_binary = image.split(';base64,')
        self.extension = self.image_format.split('/')[-1]
        return image

    def clean(self):
        super(ProductCreateForm, self).clean()
        self.code = self.cleaned_data.get("code")
        self.name = self.cleaned_data.get("name")
        self.price = self.cleaned_data.get("price")
        self.discount = self.cleaned_data.get("discount")
        self.description = self.cleaned_data.get("description")

    def is_valid(self):
        valid = super(ProductCreateForm, self).is_valid()
        return valid

    def save(self):
        image = ContentFile(base64_decode_raw(self.image_binary.encode('utf-8')), name=self.get_file_name())

        self.instance = Product(image=image, code=self.code, name=self.name, description=self.description,
                               price=self.price, discount=self.discount)
        self.instance.save()
        self.instance.create_thumbnail()

        return self.instance
    
    def get_file_name(self):
        file_name = stringify_datetime(now(), datetime_format=DateTimeFormatter.DEFAULT_FORMAT)
        return "{0}.{1}".format(file_name, self.extension)

    def get_success_message(self):
        return ADD_SUCCESS

    def get_error_message(self):
        return ADD_ERROR