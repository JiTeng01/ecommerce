from toolbox.api.serializers.serializers import serializers, BaseAPIModelSerializer, BaseSelectAPIModelSerializer
from product.models import Product


class ProductSerializer(BaseAPIModelSerializer):

    id = serializers.SerializerMethodField()
    code = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()
    thumbnail_url = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    discount = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ("id", "code", "name", "image_url", "thumbnail_url", "price", "description", "discount")
    
    def get_id(self, obj):
        return obj.id

    def get_code(self, obj):
        return obj.code

    def get_name(self, obj):
        return obj.name

    def get_price(self, obj):
        return obj.price

    def get_image_url(self, obj):
        return obj.get_image_url() if obj.image else ""

    def get_thumbnail_url(self, obj):
        return obj.get_thumbnail_url() if obj.thumbnail else ""

    def get_description(self, obj):
        return obj.description if obj.description else ""

    def get_discount(self, obj):
        return obj.discount


class ProductListSerializer(ProductSerializer):

    edit_url = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ("id", "code", "name", "image", "price", "edit_url")

    def get_edit_url(self, obj):
        return ""