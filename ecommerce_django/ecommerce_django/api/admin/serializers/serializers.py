from toolbox.api.serializers.serializers import serializers, BaseAPIModelSerializer, BaseSelectAPIModelSerializer
from epanel.constants.admin import AdminAPIURL, AdminPermission
from account.models import Account, User
from django.contrib.auth.models import Permission, Group

class AdminSerializer(BaseAPIModelSerializer):

    username = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()
    phone_number = serializers.SerializerMethodField()
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = ('username', 'full_name', "email", 'phone_number', 'permissions')

    def get_username(self, obj):
        return obj.user.username

    def get_full_name(self, obj):
        return obj.full_name if obj.full_name else "N.A."

    def get_email(self, obj):
        return obj.user.email if obj.user.email else "N.A."

    def get_phone_number(self, obj):
        return obj.phone_number if obj.phone_number else "N.A."
    
    def get_permissions(self, obj):
        account = Account.objects.filter(id=obj.id).first()
        permissions = Permission.objects.filter(user=account.user_id)
        return [item.id for item in permissions]


class AdminListSerializer(AdminSerializer):

    details_url = serializers.SerializerMethodField()
    password_url = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = AdminSerializer.Meta.fields + ("details_url", "password_url")

    def __init__(self, *args, **kwargs):
        super(AdminListSerializer, self).__init__(*args, **kwargs)
        self.request = self.context.get("request")
        self.user = self.request.user

    def get_details_url(self, obj):
        if self.user.is_superuser or self.user.has_perm(AdminPermission.EDIT_ADMIN):
            return AdminAPIURL.get_details_url(args=[obj.id])
        return ""

    def get_password_url(self, obj):
        return ''
        if self.user.is_superuser or self.user.has_perm(AdminPermission.CHANGE_ADMIN_PASSWORD):
            return AdminAPIURL.get_password_url(args=[obj.id])
        return ""

class AdminSelectSerializer(BaseAPIModelSerializer):

    text = serializers.SerializerMethodField()
    value = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = ("text", "value")

    def get_text(self, obj):
        return obj.full_name

    def get_value(self, obj):
        return obj.id

class PermissionSelectSerializer(BaseSelectAPIModelSerializer):

    text = serializers.SerializerMethodField()
    value = serializers.SerializerMethodField()

    class Meta:
        model = Permission
        fields = ("text", "value")

    def get_text(self, obj):
        return obj.name

    def get_value(self, obj):
        return obj.id
