import logging

from django.db.models import Avg
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Product, Category, Order, Customer
from .serializers import (
    ProductSerializer,
    CreateProductSerializer,
    CategorySerializer,
    CreateCategorySerializer,
    OrderSerializer,
    CreateOrderSerializer,
    CustomerSerializer,
    CreateCustomerSerializer,
)
from .tasks import mail_admin
from .utils import get_descendant_categories
from africas_talking.tasks import send_sms
from user.views import AuthenticatedAPIView
from utils.pagination import StandardPagination
from utils.open_api import page, per_page, get_paginated_response_schema


logger = logging.getLogger(__name__)


@extend_schema(tags=["Product"])
@extend_schema_view(
    get=extend_schema(
        parameters=[page, per_page],
        responses={
            200: get_paginated_response_schema(
                ProductSerializer, "Paginated list of products"
            ),
        },
    ),
    post=extend_schema(
        request=CreateProductSerializer,
    ),
)
class ProductList(AuthenticatedAPIView):
    serializer_class = ProductSerializer
    pagination_class = StandardPagination

    def get(self, request, format=None):
        """Get a paginated list of products."""
        paginator = self.pagination_class()
        products = paginator.paginate_queryset(Product.objects.all(), request)
        serializer = self.serializer_class(products, many=True)
        response = paginator.get_paginated_response(serializer.data)
        return Response(response, status=200)

    def post(self, request, format=None):
        """Create a new product."""
        serializer = CreateProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)


@extend_schema(tags=["Product"])
class ProductDetail(AuthenticatedAPIView):
    serializer_class = ProductSerializer

    def get(self, request, pk, format=None):
        """Get a product by its ID."""
        product = get_object_or_404(Product, pk=pk)
        serializer = self.serializer_class(product)
        return Response(serializer.data, status=200)

    def put(self, request, pk, format=None):
        """Update a product by its ID."""
        product = get_object_or_404(Product, pk=pk)
        serializer = self.serializer_class(product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)

    def delete(self, request, pk, format=None):
        """Delete a product by its ID."""
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return Response(status=204)


@extend_schema(tags=["Category"])
@extend_schema_view(
    get=extend_schema(
        parameters=[page, per_page],
        responses={
            200: get_paginated_response_schema(
                CategorySerializer, "Paginated list of categories"
            ),
        }
    ),
    post=extend_schema(
        request=CreateCategorySerializer,
    ),
)
class CategoryList(AuthenticatedAPIView):
    serializer_class = CategorySerializer
    pagination_class = StandardPagination

    def get(self, request, format=None):
        """Get a paginated list of categories."""
        paginator = self.pagination_class()
        categories = paginator.paginate_queryset(Category.objects.all(), request)
        serializer = self.serializer_class(categories, many=True)
        response = paginator.get_paginated_response(serializer.data)
        return Response(response, status=200)

    def post(self, request, format=None):
        """Create a new category."""
        serializer = CreateCategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)


@extend_schema(tags=["Category"])
class CategoryDetail(AuthenticatedAPIView):
    serializer_class = CategorySerializer

    def get(self, request, pk, format=None):
        """Get a category by its ID."""
        category = get_object_or_404(Category, pk=pk)
        serializer = self.serializer_class(category)
        return Response(serializer.data, status=200)

    def put(self, request, pk, format=None):
        """Update a category by its ID."""
        category = get_object_or_404(Category, pk=pk)
        serializer = self.serializer_class(category, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)

    def delete(self, request, pk, format=None):
        """Delete a category by its ID."""
        category = get_object_or_404(Category, pk=pk)
        category.delete()
        return Response(status=204)


@extend_schema(tags=["Order"])
@extend_schema_view(
    get=extend_schema(
        parameters=[page, per_page],
        responses={
            200: get_paginated_response_schema(
                OrderSerializer, "Paginated list of orders"
            ),
        }
    ),
    post=extend_schema(
        request=CreateOrderSerializer,
    ),
)
class OrderList(AuthenticatedAPIView):
    serializer_class = OrderSerializer
    pagination_class = StandardPagination

    def get(self, request, format=None):
        """Get a paginated list of orders."""
        paginator = self.pagination_class()
        orders = paginator.paginate_queryset(Order.objects.all(), request)
        serializer = self.serializer_class(orders, many=True)
        response = paginator.get_paginated_response(serializer.data)
        return Response(response, status=200)

    def post(self, request, format=None):
        """Create a new order."""
        serializer = CreateOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()

        # Send an SMS to the customer
        if order.customer.phone_number:
            send_sms.delay_on_commit(
                f"Your order has been placed.",
                [order.customer.phone_number],
            )
        else:
            logger.warning(f"No phone number for customer {order.customer.id}")

        # Send an email to the admin
        mail_admin.delay_on_commit(
            f"New Order Placed.",
            f"Order ID: {order.id} \n Total Price: {order.total_price}",
        )
        return Response(
            self.serializer_class(order).data, status=status.HTTP_201_CREATED
        )


@extend_schema(tags=["Order"])
class OrderDetail(AuthenticatedAPIView):
    serializer_class = OrderSerializer

    def get(self, request, pk, format=None):
        """Get an order by its ID."""
        order = get_object_or_404(Order, pk=pk)
        serializer = self.serializer_class(order)
        return Response(serializer.data, status=200)

    def put(self, request, pk, format=None):
        """Update an order by its ID."""
        order = get_object_or_404(Order, pk=pk)
        serializer = self.serializer_class(order, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)

    def delete(self, request, pk, format=None):
        """Delete an order by its ID."""
        order = get_object_or_404(Order, pk=pk)
        order.delete()
        return Response(status=204)


@extend_schema(tags=["Customer"])
@extend_schema_view(
    get=extend_schema(
        parameters=[page, per_page],
        responses={
            200: get_paginated_response_schema(
                CustomerSerializer, "Paginated list of customers"
            ),
        }
    ),
    post=extend_schema(
        request=CreateCustomerSerializer,
    ),
)
class CustomerList(AuthenticatedAPIView):
    serializer_class = CustomerSerializer
    pagination_class = StandardPagination

    def get(self, request, format=None):
        """Get a paginated list of customers."""
        paginator = self.pagination_class()
        customers = paginator.paginate_queryset(Customer.objects.all(), request)
        serializer = self.serializer_class(customers, many=True)
        response = paginator.get_paginated_response(serializer.data)
        return Response(response, status=200)

    def post(self, request, format=None):
        """Create a new customer."""
        serializer = CreateCustomerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)


@extend_schema(tags=["Customer"])
class CustomerDetail(AuthenticatedAPIView):
    serializer_class = CustomerSerializer

    def get(self, request, pk, format=None):
        """Get a customer by their ID."""
        customer = get_object_or_404(Customer, pk=pk)
        serializer = self.serializer_class(customer)
        return Response(serializer.data, status=200)

    def put(self, request, pk, format=None):
        """Update a customer by their ID."""
        customer = get_object_or_404(Customer, pk=pk)
        serializer = self.serializer_class(customer, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)

    def delete(self, request, pk, format=None):
        """Delete a customer by their ID."""
        customer = get_object_or_404(Customer, pk=pk)
        customer.delete()
        return Response(status=204)


@extend_schema(tags=["Category"])
class AverageProductPrice(APIView):
    def get(self, request, pk, format=None):
        """
        Return the average product price for a given category and its
        child categories.
        """
        # Get the main category
        category = get_object_or_404(Category, pk=pk)

        # Get all descendant categories (including the main category)
        all_categories = [category] + get_descendant_categories(category)

        # Get all products in the category and its descendants
        products = Product.objects.filter(category__in=all_categories)

        # Calculate the average price
        average_price = products.aggregate(Avg("price"))["price__avg"]

        # Return the response
        return Response({"average_price": average_price}, status=200)
