from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.response import Response
from toolbox.api.permissions import IsLoggedInPermission, IsTokenExistPermission
from toolbox.api.responses import success_response, error_response
from api.product.forms import ProductListForm, ProductCreateForm, ProductRetrieveForm, ProductUpdateForm
from api.product.serializers import ProductHeader, ProductListSerializer, ProductSerializer


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

class ProductRetrieveUpdateAPIView(RetrieveAPIView, UpdateAPIView):
    serializer_class = ProductSerializer
    permission_classes = (IsLoggedInPermission, IsTokenExistPermission)

    def get_request_data(self):
        request_data = dict(instance=self.kwargs.get(self.lookup_field))

        if self.request.method == "PUT":
            fields = ["name", "price", "description", "discount", "image"]
            for field in fields:
                request_data[field] = self.request.data.get(field, "")

        return request_data

    def retrieve(self, request, *args, **kwargs):
        form, header = ProductRetrieveForm(self.get_request_data(), request=request), ProductHeader()
        if form.is_valid():
            serializer = self.get_serializer(form.get_object())
            response = success_response(dict(object=serializer.data))
        else:
            response = error_response(dict(object=dict()))

        return Response(response)

    def update(self, request, *args, **kwargs):
        form = ProductUpdateForm(self.get_request_data(), request=request)
        if form.is_valid():
            serializer = self.get_serializer(form.save())
            response = success_response(dict(object=serializer.data, message=form.get_success_message()))
        else:
            response = error_response(dict(errors=form.errors, message=form.get_error_message()))

        return Response(response)