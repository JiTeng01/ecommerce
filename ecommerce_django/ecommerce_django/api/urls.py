from django.urls import path, include


urlpatterns = [
    path("admin/", include(("api.admin.urls", "admin"), namespace="admin")),
    path("product/", include(("api.product.urls", "product"), namespace="product")),
    path("", include(("api.account.urls", "login"), namespace="login")),
]
