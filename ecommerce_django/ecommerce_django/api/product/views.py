from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.response import Response
from toolbox.api.permissions import IsLoggedInPermission, IsTokenExistPermission
from toolbox.api.responses import success_response, error_response
from api.product.forms import ProductListForm, ProductCreateForm
from api.product.serializers import ProductHeader, ProductListSerializer


class ProductListCreateAPIView(ListAPIView, CreateAPIView):
    serializer_class = ProductListSerializer
    permission_classes = (IsLoggedInPermission, IsTokenExistPermission)

    def list(self, request, *args, **kwargs):
        form, header = ProductListForm(request.GET), ProductHeader()
        if form.is_valid():
            serializer = self.get_serializer(form.get_items(), many=True)
            response = success_response(dict(items=serializer.data, headers=header.get_headers()))
        else:
            response = error_response(dict(items=[], headers=header.get_headers()))

        response.update(dict(pagination=form.get_pagination()))

        return Response(response)
    
    def create(self, request, *args, **kwargs):
        form = ProductCreateForm(request.data)
        if form.is_valid():
            form.save()
            response = success_response(dict(message=form.get_success_message()))
        else:
            response = error_response(dict(errors=form.errors, message=form.get_error_message()))

        return Response(response)