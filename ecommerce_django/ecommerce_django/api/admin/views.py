from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response
from toolbox.api.permissions import IsLoggedInPermission, IsTokenExistPermission
from toolbox.api.responses import success_response, error_response
from api.admin.forms import AdminListForm, AdminCreateForm, AdminUpdateForm, AdminDeleteForm
from api.admin.serializers import AdminHeader, AdminSerializer, AdminListSerializer, PermissionSelectSerializer
from django.contrib.auth.models import Permission, Group


class AdminListCreateAPIView(ListAPIView, CreateAPIView):
    queryset = AdminListForm.get_all()
    serializer_class = AdminListSerializer
    permission_classes = (IsLoggedInPermission, IsTokenExistPermission)

    def list(self, request, *args, **kwargs):
        form, header = AdminListForm(self.request.GET, request=request), AdminHeader()
        if form.is_valid():
            serializer = self.get_serializer(form.get_items(), many=True)
            response = success_response(dict(items=serializer.data, headers=header.get_headers()))
        else:
            response = error_response(dict(items=[], headers=header.get_headers()))
        permission_serializer = PermissionSelectSerializer(Permission.objects.all().order_by('id'), many=True)
        response.update(dict(pagination=form.get_pagination(), permissions=form.get_permissions(),
                             roles=form.get_roles(), permission_list=permission_serializer.data))
        return Response(response)
    
    def create(self, request, *args, **kwargs):
        form = AdminCreateForm(self.request.data, request=request)
        if form.is_valid():
            form.save()
            response = success_response(dict(message=form.get_success_message()))
        else:
            response = error_response(dict(errors=form.errors, message=form.get_error_message()))

        return Response(response)

class AdminUpdateDestroyAPIView(UpdateAPIView, DestroyAPIView):
    serializer_class = AdminSerializer
    permission_classes = (IsLoggedInPermission, IsTokenExistPermission)
    
    def get_request_data(self):
        request_data = self.request.data
        if self.request.method=='PUT':
            return dict(email=request_data.get("email"), full_name=request_data.get("full_name"),
                    phone_number=request_data.get("phone_number"), permissions=self.request.data.get("permissions", ""), 
                    pk=self.kwargs.get(self.lookup_field))
        else:
           return dict(instance=self.kwargs.get(self.lookup_field))
    
    def update(self, request, *args, **kwargs):
        form = AdminUpdateForm(self.get_request_data(), request=request)
        if form.is_valid():
            form.save()
            response = success_response(dict(message=form.get_success_message()))
        else:
            response = error_response(dict(errors=form.errors, message=form.get_error_message()))

        return Response(response)
    
    def destroy(self, request, *args, **kwargs):
        form = AdminDeleteForm(self.get_request_data(), request=request)

        if form.is_valid():
            form.delete()
            response = success_response(dict(message=form.get_success_message()))
        else:
            response = error_response(dict(errors=form.errors, message=form.get_error_message()))

        return Response(response)

