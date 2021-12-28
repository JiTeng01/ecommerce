from toolbox.aws.storages import PrivateMediaStorage


class ProductPrivateStorage(PrivateMediaStorage):

    def get_available_name(self, name, max_length=None):
        self.get_location(name)
        return super().get_available_name(name, max_length)

    def url(self, name, parameters=None, expire=None):
        self.get_location(name)
        return super(ProductPrivateStorage, self).url(name, parameters=parameters, expire=expire)

    def get_location(self, name):
        self.location = "product/"

