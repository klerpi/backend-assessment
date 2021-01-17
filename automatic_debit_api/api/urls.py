from django.urls import path

from .views.external_app_views import (
    ProductListAPIView,
    ProductDetailAPIView,
    ProductActivationRequestAPIView,
    ProductActivationCancelationAPIView,
)

urlpatterns = [
    path("products/", ProductListAPIView.as_view(), name="product_list"),
    path("products/<int:pk>/", ProductDetailAPIView.as_view(), name="product_detail"),
    path(
        "products/<int:pk>/activate/",
        ProductActivationRequestAPIView.as_view(),
        name="product_activate",
    ),
    path(
        "products/<int:pk>/cancel/",
        ProductActivationCancelationAPIView.as_view(),
        name="product_cancel",
    ),
]
