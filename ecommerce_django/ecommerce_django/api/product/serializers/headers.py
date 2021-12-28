from toolbox.api.serializers.headers import BaseTableHeader


class ProductHeader:

    sn = BaseTableHeader("S/N", "sn")
    image = BaseTableHeader("Product Image", "productimage")
    name = BaseTableHeader("Name", "name")
    code = BaseTableHeader("Code", "code")
    price = BaseTableHeader("Price", "price")
    action = BaseTableHeader("Action", "action")

    class Meta:
        fields = ["sn", "code", "name", "image", "price", "action"]

    def get_headers(self):
        return [getattr(self, field).__dict__ for field in self.Meta.fields]
