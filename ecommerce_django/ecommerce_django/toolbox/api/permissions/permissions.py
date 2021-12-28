from django.contrib.auth import get_user_model
from rest_framework import permissions
from toolbox.api.exceptions.exceptions import *


class ExemptCheckPermission(permissions.BasePermission):
    """
        Not required to check the permission
    """
    def has_permission(self, request, view):
        return True


class ConditionalExemptCheckPermission(permissions.BasePermission):

    def has_permission(self, request, view):

        if not isinstance(request.user, get_user_model()):
            return True

        authorization = request.META.get('HTTP_AUTHORIZATION', None)

        if authorization is None or not authorization:
            raise NotAuthenticated()

        if 'Token' not in authorization:
            raise NotAuthenticated()

        User = get_user_model()
        token = authorization.replace("Token ", "").strip()
        user = User.objects.get_one_by_token(token)

        if not isinstance(user, User):
            raise NotAuthenticated()

        if user.is_expired:
            raise ExpiredAuthenticationToken()

        return True


class IsLoggedInPermission(permissions.BasePermission):
    """
        Check whether a user has logged in
        If logged in, then the user has a permission to do
        If not, reject the request
    """

    def has_permission(self, request, view):
        if not isinstance(request.user, get_user_model()):
            raise AuthenticationLoginFailed()
        return True


class IsTokenExistPermission(permissions.BasePermission):
    """
        Check whether a user has logged in
        If logged in, then the user has a permission to do
        If not, reject the request
    """

    def has_permission(self, request, view):

        authorization = request.META.get('HTTP_AUTHORIZATION', None)
        if authorization is None or not authorization:
            raise NotAuthenticated()

        if 'Token' not in authorization:
            raise NotAuthenticated()
        User = get_user_model()
        # token = authorization.replace("Token ", "").strip()
        user = User.objects.get_one_by_token(request.session["accesstoken"])
        if not isinstance(user, User):
            raise NotAuthenticated()

        if user.is_expired:
            raise ExpiredAuthenticationToken()

        return True


class HasTokenPermission(permissions.BasePermission):
    """
        Check whether a user has a token
    """

    def has_permission(self, request, view):

        authorization = request.META.get('HTTP_AUTHORIZATION', None)

        if authorization is None or not authorization:
            raise NotAuthenticated()

        token = authorization.replace("Token ", "").strip()
        if not get_user_model().objects.token_exist(token):
            raise NotAuthenticated()

        return True




