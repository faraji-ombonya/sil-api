from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.response import Response

from shop.models import Product, Category, Order, Customer
from shop.serializers import (
    ProductSerializer,
    CategorySerializer,
    OrderSerializer,
    CustomerSerializer,
)
from user.views import AuthenticatedAPIView
from utils.pagination import StandardPagination
from utils.helpers import get_paginated_response_schema


@extend_schema(tags=["Product"])
class ProductList(AuthenticatedAPIView):
    serializer_class = ProductSerializer
    pagination_class = StandardPagination

    @extend_schema(
        responses={
            200: get_paginated_response_schema(
                ProductSerializer, "Paginated list of products"
            ),
        }
    )
    def get(self, request, format=None):
        paginator = self.pagination_class()
        products = paginator.paginate_queryset(Product.objects.all(), request)
        serializer = self.serializer_class(products, many=True)
        response = paginator.get_paginated_response(serializer.data)
        return Response(response, status=200)

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)


@extend_schema(tags=["Product"])
class ProductDetail(AuthenticatedAPIView):
    serializer_class = ProductSerializer

    def get(self, request, pk, format=None):
        product = get_object_or_404(Product, pk=pk)
        serializer = self.serializer_class(product)
        return Response(serializer.data, status=200)

    def put(self, request, pk, format=None):
        product = get_object_or_404(Product, pk=pk)
        serializer = self.serializer_class(product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)

    def delete(self, request, pk, format=None):
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return Response(status=204)


@extend_schema(tags=["Category"])
class CategoryList(APIView):
    serializer_class = CategorySerializer

    def get(self, request, format=None):
        categories = Category.objects.all()
        serializer = self.serializer_class(categories, many=True)
        return Response(serializer.data, status=200)

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)


@extend_schema(tags=["Category"])
class CategoryDetail(AuthenticatedAPIView):
    serializer_class = CategorySerializer

    def get(self, request, pk, format=None):
        category = get_object_or_404(Category, pk=pk)
        serializer = self.serializer_class(category)
        return Response(serializer.data, status=200)

    def put(self, request, pk, format=None):
        category = get_object_or_404(Category, pk=pk)
        serializer = self.serializer_class(category, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)

    def delete(self, request, pk, format=None):
        category = get_object_or_404(Category, pk=pk)
        category.delete()
        return Response(status=204)


@extend_schema(tags=["Order"])
class OrderList(AuthenticatedAPIView):
    serializer_class = OrderSerializer
    pagination_class = StandardPagination

    @extend_schema(
        responses={
            200: get_paginated_response_schema(
                OrderSerializer, "Paginated list of orders"
            ),
        }
    )
    def get(self, request, format=None):
        paginator = self.pagination_class()
        orders = paginator.paginate_queryset(Order.objects.all(), request)
        serializer = self.serializer_class(orders, many=True)
        response = paginator.get_paginated_response(serializer.data)
        return Response(response, status=200)

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)


@extend_schema(tags=["Order"])
class OrderDetail(AuthenticatedAPIView):
    serializer_class = OrderSerializer

    def get(self, request, pk, format=None):
        order = get_object_or_404(Order, pk=pk)
        serializer = self.serializer_class(order)
        return Response(serializer.data, status=200)

    def put(self, request, pk, format=None):
        order = get_object_or_404(Order, pk=pk)
        serializer = self.serializer_class(order, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)

    def delete(self, request, pk, format=None):
        order = get_object_or_404(Order, pk=pk)
        order.delete()
        return Response(status=204)


@extend_schema(tags=["Customer"])
class CustomerList(AuthenticatedAPIView):
    serializer_class = CustomerSerializer
    pagination_class = StandardPagination

    @extend_schema(
        responses={
            200: get_paginated_response_schema(
                CustomerSerializer, "Paginated list of customers"
            ),
        }
    )
    def get(self, request, format=None):
        paginator = self.pagination_class()
        customers = paginator.paginate_queryset(Customer.objects.all(), request)
        serializer = self.serializer_class(customers, many=True)
        response = paginator.get_paginated_response(serializer.data)
        return Response(response, status=200)

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)


@extend_schema(tags=["Customer"])
class CustomerDetail(AuthenticatedAPIView):
    serializer_class = CustomerSerializer

    def get(self, request, pk, format=None):
        customer = get_object_or_404(Customer, pk=pk)
        serializer = self.serializer_class(customer)
        return Response(serializer.data, status=200)

    def put(self, request, pk, format=None):
        customer = get_object_or_404(Customer, pk=pk)
        serializer = self.serializer_class(customer, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)

    def delete(self, request, pk, format=None):
        customer = get_object_or_404(Customer, pk=pk)
        customer.delete()
        return Response(status=204)
