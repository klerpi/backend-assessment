from django.urls import path

from .views.external_app_views import (
    ProductListAPIView,
    ProductDetailAPIView,
    ProductActivationRequestAPIView,
)

urlpatterns = [
    path("products/", ProductListAPIView.as_view(), name="product_list"),
    path("products/<int:pk>/", ProductDetailAPIView.as_view(), name="product_detail"),
    path(
        "products/<int:pk>/activate/",
        ProductActivationRequestAPIView.as_view(),
        name="product_activate",
    ),
]
