from toolbox.api.serializers.serializers import serializers, BaseAPIModelSerializer
from account.models import Account


class AccountProfileSerializer(BaseAPIModelSerializer):

    username = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    contact_number = serializers.SerializerMethodField()
    nric = serializers.SerializerMethodField()
    
    class Meta:
        model = Account
        fields = ("username", "email", "first_name", "last_name", "contact_number", "nric")

    def get_username(self, obj):
        return obj.user.username

    def get_email(self, obj):
        return obj.user.email

    def get_first_name(self, obj):
        return obj.first_name if obj.first_name else ""

    def get_last_name(self, obj):
        return obj.last_name if obj.last_name else ""

    def get_contact_number(self, obj):
        return obj.contact_number if obj.contact_number else ""

    def get_nric(self, obj):
        return obj.get_nric_display()
