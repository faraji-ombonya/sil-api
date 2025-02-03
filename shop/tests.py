from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Category, Product, Customer

# class CategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = "__all__"


# @extend_schema(tags=["Category"])
# @extend_schema_view(
#     get=extend_schema(
#         responses={
#             200: get_paginated_response_schema(
#                 CategorySerializer, "Paginated list of categories"
#             ),
#         }
#     ),
# )
# class CategoryList(APIView):
#     serializer_class = CategorySerializer
#     pagination_class = StandardPagination

#     def get(self, request, format=None):
#         paginator = self.pagination_class()
#         categories = paginator.paginate_queryset(Category.objects.all(), request)
#         serializer = self.serializer_class(categories, many=True)
#         response = paginator.get_paginated_response(serializer.data)
#         return Response(response, status=200)

#     def post(self, request, format=None):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=201)


# @extend_schema(tags=["Category"])
# class CategoryDetail(AuthenticatedAPIView):
#     serializer_class = CategorySerializer

#     def get(self, request, pk, format=None):
#         category = get_object_or_404(Category, pk=pk)
#         serializer = self.serializer_class(category)
#         return Response(serializer.data, status=200)

#     def put(self, request, pk, format=None):
#         category = get_object_or_404(Category, pk=pk)
#         serializer = self.serializer_class(category, data=request.data, partial=True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=200)

#     def delete(self, request, pk, format=None):
#         category = get_object_or_404(Category, pk=pk)
#         category.delete()
#         return Response(status=204)

# class Category(BaseModel):
#     name = models.CharField(max_length=255)
#     slug = models.SlugField(unique=True)
#     parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)

#     # slugify the name
#     def save(self, *args, **kwargs):
#         self.slug = slugify(self.name)
#         super().save(*args, **kwargs)

# from django.urls import path

# from shop import views


# urlpatterns = [
#     path("products/", views.ProductList.as_view(), name="product_list"),
#     path("products/<uuid:pk>/", views.ProductDetail.as_view(), name="product_detail"),
#     path("categories/", views.CategoryList.as_view(), name="category_list"),
#     path(
#         "categories/<uuid:pk>/", views.CategoryDetail.as_view(), name="category_detail"
#     ),
#     path("orders/", views.OrderList.as_view(), name="order_list"),
#     path("orders/<uuid:pk>/", views.OrderDetail.as_view(), name="order_detail"),
#     path("customers/", views.CustomerList.as_view(), name="customer_list"),
#     path(
#         "customers/<uuid:pk>/", views.CustomerDetail.as_view(), name="customer_detail"
#     ),
# ]


class CategoryTestCase(APITestCase):
    def setUp(self):
        User = get_user_model()
        test_user = User.objects.create_user(
            email="testuser@test.com", password="testpassword"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=test_user)
        self.list_endpoint = reverse("category_list")
        self.detail_endpoint = lambda id: reverse("category_detail", args=[id])

        categories = [
            {"name": "Category 1"},
            {"name": "Category 2"},
            {"name": "Category 3"},
            {"name": "Category 4"},
            {"name": "Category 5"},
            {"name": "Category 6"},
        ]

        for category in categories:
            Category.objects.create(**category)

        self.category_g = Category.objects.first()

    def test_create_category(self):
        endpoint = self.list_endpoint
        data = {"name": "Category x"}
        response = self.client.post(endpoint, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_categories(self):
        endpoint = self.list_endpoint
        response = self.client.get(endpoint, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_category(self):
        endpoint = self.detail_endpoint(self.category_g.id)
        response = self.client.get(endpoint, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_category(self):
        endpoint = self.detail_endpoint(self.category_g.id)
        data = {"name": "Category x"}
        response = self.client.put(endpoint, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_category(self):
        endpoint = self.detail_endpoint(self.category_g.id)
        response = self.client.delete(endpoint, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


# class Product(BaseModel):
#     name = models.CharField(max_length=255)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     description = models.TextField()
#     image = models.URLField(null=True, blank=True)
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)


class ProductTestCase(APITestCase):
    def setUp(self):
        User = get_user_model()
        test_user = User.objects.create_user(
            email="testuser@test.com", password="testpassword"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=test_user)
        self.list_endpoint = reverse("product_list")
        self.detail_endpoint = lambda id: reverse("product_detail", args=[id])

        self.category_x = Category.objects.create(
            name="Category X",
        )

        self.product_x = Product.objects.create(
            name="Product X",
            description="Product X description",
            category=self.category_x,
            price=100,
            image="https://via.placeholder.com/150",
        )

    def test_create_product(self):
        endpoint = self.list_endpoint
        data = {
            "name": "Product Y",
            "description": "Product Y description",
            "category": self.category_x.id,
            "price": 100,
            "image": "https://via.placeholder.com/150",
        }
        response = self.client.post(endpoint, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_products(self):
        endpoint = self.list_endpoint
        response = self.client.get(endpoint, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_product(self):
        endpoint = self.detail_endpoint(self.product_x.id)
        response = self.client.get(endpoint, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_product(self):
        endpoint = self.detail_endpoint(self.product_x.id)
        data = {
            "name": "Product new x",
            "description": "Product x description",
            "category": self.category_x.id,
            "price": 100,
            "image": "https://via.placeholder.com/150",
        }
        response = self.client.put(endpoint, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Product new x")

    def test_delete_product(self):
        endpoint = self.detail_endpoint(self.product_x.id)
        response = self.client.delete(endpoint, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class CustomerTestCase(APITestCase):
    def setUp(self):
        User = get_user_model()
        test_user = User.objects.create_user(
            email="testuser@test.com", password="testpassword"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=test_user)
        self.list_endpoint = reverse("customer_list")
        self.detail_endpoint = lambda id: reverse("customer_detail", args=[id])

        self.customer_x = Customer.objects.create(
            user=test_user,
            phone_number="1234567890",
        )

        self.test_user_x = User.objects.create_user(
            email="testuserx@test.com", password="testpasswordx"
        )

    def test_create_customer(self):
        data = {"user": self.test_user_x.id, "phone_number": "1234567890"}
        response = self.client.post(self.list_endpoint, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_customers(self):
        response = self.client.get(self.list_endpoint, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_customer(self):
        response = self.client.get(
            self.detail_endpoint(self.customer_x.id), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_customer(self):
        data = {"phone_number": "1234567890"}
        response = self.client.put(
            self.detail_endpoint(self.customer_x.id), data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["phone_number"], "1234567890")

    def test_delete_customer(self):
        response = self.client.delete(
            self.detail_endpoint(self.customer_x.id), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class OrderTestCase(APITestCase):
    def setUp(self):
        User = get_user_model()
        test_user = User.objects.create_user(
            email="testuser@test.com", password="testpassword"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=test_user)
        self.list_endpoint = reverse("order_list")
        self.detail_endpoint = lambda id: reverse("order_detail", args=[id])

        self.customer_x = Customer.objects.create(
            user=test_user, phone_number="1234567890"
        )

        self.category_x = Category.objects.create(
            name="Category x",
        )

        self.product_x = Product.objects.create(
            name="Product x",
            description="Product x description",
            category=self.category_x,
            price=100,
            image="https://via.placeholder.com/150",
        )

    def test_create_order(self):
        data = {
            "customer": self.customer_x.id,
            "order_items": [{"product": self.product_x.id, "quantity": 4}],
        }
        response = self.client.post(self.list_endpoint, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["customer"], self.customer_x.id)
        self.assertEqual(
            response.data["order_items"][0]["product"]["id"], str(self.product_x.id)
        )
        self.assertEqual(response.data["order_items"][0]["quantity"], 4)

    def test_get_orders(self):
        data = {
            "customer": self.customer_x.id,
            "order_items": [{"product": self.product_x.id, "quantity": 4}],
        }
        response = self.client.post(self.list_endpoint, data, format="json")
        response = self.client.get(self.list_endpoint, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_order(self):
        data = {
            "customer": self.customer_x.id,
            "order_items": [{"product": self.product_x.id, "quantity": 4}],
        }
        response = self.client.post(self.list_endpoint, data, format="json")
        order_id = response.data["id"]
        response = self.client.get(self.detail_endpoint(order_id), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_order(self):
        data = {
            "customer": self.customer_x.id,
            "order_items": [{"product": self.product_x.id, "quantity": 5}],
        }
        response = self.client.post(self.list_endpoint, data, format="json")
        order_id = response.data["id"]
        response = self.client.delete(self.detail_endpoint(order_id), format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
