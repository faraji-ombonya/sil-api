from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Product, Category, Order, Customer
from .serializers import (
    ProductSerializer,
    CategorySerializer,
    OrderSerializer,
    CustomerSerializer,
)
from .tasks import mail_admin
from africas_talking.tasks import send_sms
from user.views import AuthenticatedAPIView
from utils.pagination import StandardPagination
from utils.helpers import get_paginated_response_schema


@extend_schema(tags=["Product"])
@extend_schema_view(
    get=extend_schema(
        responses={
            200: get_paginated_response_schema(
                ProductSerializer, "Paginated list of products"
            ),
        }
    ),
)
class ProductList(AuthenticatedAPIView):
    serializer_class = ProductSerializer
    pagination_class = StandardPagination

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
@extend_schema_view(
    get=extend_schema(
        responses={
            200: get_paginated_response_schema(
                CategorySerializer, "Paginated list of categories"
            ),
        }
    ),
)
class CategoryList(APIView):
    serializer_class = CategorySerializer
    pagination_class = StandardPagination

    def get(self, request, format=None):
        paginator = self.pagination_class()
        categories = paginator.paginate_queryset(Category.objects.all(), request)
        serializer = self.serializer_class(categories, many=True)
        response = paginator.get_paginated_response(serializer.data)
        return Response(response, status=200)

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
@extend_schema_view(
    get=extend_schema(
        responses={
            200: get_paginated_response_schema(
                OrderSerializer, "Paginated list of orders"
            ),
        }
    ),
)
class OrderList(AuthenticatedAPIView):
    serializer_class = OrderSerializer
    pagination_class = StandardPagination

    def get(self, request, format=None):
        paginator = self.pagination_class()
        orders = paginator.paginate_queryset(Order.objects.all(), request)
        serializer = self.serializer_class(orders, many=True)
        response = paginator.get_paginated_response(serializer.data)
        return Response(response, status=200)

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()

        # Send SMS to the customer
        send_sms.delay_on_commit(
            f"Your order {order.id} has been placed.",
            [order.customer.user.phone_number],
        )

        # Send email to the admin
        mail_admin.delay_on_commit(
            f"New order {order.id} has been placed.",
            f"Order ID: {order.id} \n Order Total: {order.total}",
        )
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
@extend_schema_view(
    get=extend_schema(
        responses={
            200: get_paginated_response_schema(
                CustomerSerializer, "Paginated list of customers"
            ),
        }
    ),
)
class CustomerList(AuthenticatedAPIView):
    serializer_class = CustomerSerializer
    pagination_class = StandardPagination

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
