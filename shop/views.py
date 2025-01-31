from django.shortcuts import get_object_or_404
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


class ProductList(AuthenticatedAPIView):
    serializer_class = ProductSerializer

    def get(self, request, format=None):
        page = request.GET.get("page", 1)
        per_page = request.GET.get("per_page", 10)
        offset = (int(page) - 1) * int(per_page)
        limit = offset + int(per_page)
        products = Product.objects.all()
        count = products.count()
        serializer = ProductSerializer(products[offset:limit], many=True)
        response = {
            "page": page,
            "per_page": per_page,
            "count": count,
            "results": serializer.data,
        }
        return Response(response, status=200)

    def post(self, request, format=None):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class ProductDetail(AuthenticatedAPIView):
    serializer_class = ProductSerializer

    def get(self, request, pk, format=None):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=200)

    def put(self, request, pk, format=None):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)

    def delete(self, request, pk, format=None):
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return Response(status=204)


class CategoryList(APIView):
    serializer_class = CategorySerializer

    def get(self, request, format=None):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=200)

    def post(self, request, format=None):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class CategoryDetail(AuthenticatedAPIView):
    serializer_class = CategorySerializer

    def get(self, request, pk, format=None):
        category = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=200)

    def put(self, request, pk, format=None):
        category = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(category, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)

    def delete(self, request, pk, format=None):
        category = get_object_or_404(Category, pk=pk)
        category.delete()
        return Response(status=204)


class OrderList(AuthenticatedAPIView):
    serializer_class = OrderSerializer

    def get(self, request, format=None):
        page = request.GET.get("page", 1)
        per_page = request.GET.get("per_page", 10)
        offset = (int(page) - 1) * int(per_page)
        limit = offset + int(per_page)
        orders = Order.objects.all()
        count = orders.count()
        serializer = OrderSerializer(orders[offset:limit], many=True)
        response = {
            "page": page,
            "per_page": per_page,
            "count": count,
            "results": serializer.data,
        }
        return Response(response, status=200)

    def post(self, request, format=None):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class OrderDetail(AuthenticatedAPIView):
    serializer_class = OrderSerializer

    def get(self, request, pk, format=None):
        order = get_object_or_404(Order, pk=pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=200)

    def put(self, request, pk, format=None):
        order = get_object_or_404(Order, pk=pk)
        serializer = OrderSerializer(order, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)

    def delete(self, request, pk, format=None):
        order = get_object_or_404(Order, pk=pk)
        order.delete()
        return Response(status=204)


class CustomerList(AuthenticatedAPIView):
    serializer_class = CustomerSerializer

    def get(self, request, format=None):
        page = request.GET.get("page", 1)
        per_page = request.GET.get("per_page", 10)
        offset = (int(page) - 1) * int(per_page)
        limit = offset + int(per_page)
        customers = Customer.objects.all()
        count = customers.count()
        serializer = CustomerSerializer(customers[offset:limit], many=True)
        response = {
            "page": page,
            "per_page": per_page,
            "count": count,
            "results": serializer.data,
        }
        return Response(response, status=200)

    def post(self, request, format=None):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class CustomerDetail(AuthenticatedAPIView):
    serializer_class = CustomerSerializer

    def get(self, request, pk, format=None):
        customer = get_object_or_404(Customer, pk=pk)
        serializer = CustomerSerializer(customer)
        return Response(serializer.data, status=200)

    def put(self, request, pk, format=None):
        customer = get_object_or_404(Customer, pk=pk)
        serializer = CustomerSerializer(customer, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)

    def delete(self, request, pk, format=None):
        customer = get_object_or_404(Customer, pk=pk)
        customer.delete()
        return Response(status=204)
