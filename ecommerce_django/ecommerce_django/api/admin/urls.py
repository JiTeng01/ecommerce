from django.urls import path, include
from api.admin import views


urlpatterns = [
    path('<int:pk>/', views.AdminUpdateDestroyAPIView.as_view(), name="details"),
    path('', views.AdminListCreateAPIView.as_view(), name="list"),
]