from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from toolbox.api.authentications import ExemptAuthenticationPermission
from toolbox.api.permissions import ExemptCheckPermission
from toolbox.api.responses import success_response, error_response
from api.account.forms import AccountLoginForm


class AccountLoginAPIView(CreateAPIView):
    authentication_classes = (ExemptAuthenticationPermission, )
    permission_classes = (ExemptCheckPermission, )

    def create(self, request, *args, **kwargs):
        form = AccountLoginForm(self.request.data)
        if form.is_valid():
            form.login(request)
            response = success_response(dict(token=form.get_access_token(request)))
        else:
            response = error_response(dict(errors=form.errors, message=form.get_error_message()))

        return Response(response)
