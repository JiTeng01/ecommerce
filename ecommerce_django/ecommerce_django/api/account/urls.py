from django.urls import path, include
from api.account import views


urlpatterns = [
    path("login/", views.AccountLoginAPIView.as_view(), name="login")
]