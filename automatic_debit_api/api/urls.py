from django.urls import path

from .views.external_app_views import (
    ProductListAPIView,
    ProductDetailAPIView,
    ProductActivationRequestAPIView,
    ProductActivationCancelationAPIView,
    PendingProductsAPIView,
)

from .views.superuser_views import ApproveProductAPIView, RejectProductAPIView

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
    path(
        "products/pending/",
        PendingProductsAPIView.as_view(),
        name="product_pending_list",
    ),
    path(
        "products/<int:pk>/approve/",
        ApproveProductAPIView.as_view(),
        name="product_approve",
    ),
    path(
        "products/<int:pk>/reject/",
        RejectProductAPIView.as_view(),
        name="product_reject",
    ),
]
