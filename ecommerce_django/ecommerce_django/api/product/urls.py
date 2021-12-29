from django.urls import path, include
from api.product import views


urlpatterns = [
    path("<int:pk>/", views.ProductRetrieveUpdateAPIView.as_view(), name="details"),
    path('', views.ProductListCreateAPIView.as_view(), name="list"),
]