from toolbox.db.models import models, BaseModelQuerySet, BaseModelManager, BaseModel, AWSImageModel
from toolbox.utilities.datetime import now, stringify_datetime, DateTimeFormatter
from toolbox.utilities.encodes import json_decode
from toolbox.utilities.os import os
from product.storages import ProductPrivateStorage


class ProductQuerySet(BaseModelQuerySet):

    def code(self, code):
        return self.filter(code=code)

    def code_icontain(self, code):
        return self.filter(code__icontains=code)

    def name(self, name):
        return self.filter(name=name)

    def name_icontains(self, name):
        return self.filter(name__icontains=name)


class ProductManaer(BaseModelManager):

    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def get_one_by_code(self, code):
        return self.get_all().code(code).first()

    def get_one_by_name(self, name):
        return self.get_all().name(name).first()


def get_product_name(instance, filename):
    time = stringify_datetime(now(), DateTimeFormatter.DEFAULT_FORMAT3)
    name, extension = os.path.splitext(filename)
    return time + extension


class Product(BaseModel, AWSImageModel):
    code = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    price = models.FloatField(default=0.0)
    discount = models.IntegerField(default=0)
    image = models.FileField(null=True, upload_to=get_product_name, storage=ProductPrivateStorage())
    thumbnail = models.FileField(null=True, storage=ProductPrivateStorage(), verbose_name="Thumbnail")
    description = models.TextField(blank=True, null=True)
    meta_data = models.TextField(blank=True, null=True)

    objects = ProductManaer()

    class Meta:
        db_table = "product_product"

