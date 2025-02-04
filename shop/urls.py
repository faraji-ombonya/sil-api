from django.urls import path

from shop import views


urlpatterns = [
    path("products/", views.ProductList.as_view(), name="product_list"),
    path("products/<uuid:pk>/", views.ProductDetail.as_view(), name="product_detail"),
    path("categories/", views.CategoryList.as_view(), name="category_list"),
    path(
        "categories/<uuid:pk>/", views.CategoryDetail.as_view(), name="category_detail"
    ),
    path(
        "categories/<uuid:pk>/average-price/",
        views.AverageProductPrice.as_view(),
        name="average_product_price",
    ),
    path("orders/", views.OrderList.as_view(), name="order_list"),
    path("orders/<uuid:pk>/", views.OrderDetail.as_view(), name="order_detail"),
    path("customers/", views.CustomerList.as_view(), name="customer_list"),
    path(
        "customers/<uuid:pk>/", views.CustomerDetail.as_view(), name="customer_detail"
    ),
]
