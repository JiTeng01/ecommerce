from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import AnonymousUser


class CookieProcessingMiddleware(MiddlewareMixin):

    def process_response(self, request, response):
        if not request.COOKIES.get('accesstoken') and not isinstance(request.user, AnonymousUser):
            response.set_cookie('accesstoken', request.user.token)
        elif request.COOKIES.get('accesstoken') and isinstance(request.user, AnonymousUser):
            response.delete_cookie('accesstoken')
        return response
