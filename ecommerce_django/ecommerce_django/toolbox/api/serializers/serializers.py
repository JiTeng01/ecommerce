from rest_framework import serializers
from django.contrib.auth import get_user_model


class BaseAPIModelSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        super(BaseAPIModelSerializer, self).__init__(*args, **kwargs)
        self.request = self.context.get('request', None)
        self.user = self.request.user if self.request else None

    def has_permission(self, permission_name):
        return False if not isinstance(self.user, get_user_model()) else self.user.has_perm(permission_name)

    def get_errors(self):
        error_dict = dict()
        for field_name, errors in self.errors.items():
            if field_name not in error_dict:
                error_dict[field_name] = []
            for error in errors:
                error_dict[field_name].append(str(error))
        return error_dict


class BaseSelectAPIModelSerializer(serializers.ModelSerializer):

    id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    class Meta:
        model = None
        fields = ('id', 'name')

    def get_id(self, obj):
        return obj.id
