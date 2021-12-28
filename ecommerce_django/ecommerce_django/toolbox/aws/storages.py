from storages.backends.s3boto3 import S3Boto3Storage


class BaseStaticStorage(S3Boto3Storage):

    path = ''

    def get_location(self, name):
        pass


class PublicMediaStorage(BaseStaticStorage):
    default_acl = 'public-read'
    file_overwrite = False


class PrivateMediaStorage(BaseStaticStorage):
    default_acl = 'private'
    file_overwrite = False
    custom_domain = False
