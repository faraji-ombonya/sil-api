from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from unittest.mock import patch

from .models import Category, Product, Customer, Order
from .tasks import mail_admin


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

        # User without phone number
        user_without_phone_number = User.objects.create_user(
            email="testuserx@test.com", password="testpasswordx"
        )

        # Customer without phone number
        self.customer_without_phone_number = Customer.objects.create(
            user=user_without_phone_number, phone_number=None
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

    @patch("shop.views.mail_admin.delay_on_commit")
    @patch("africas_talking.tasks.send_sms.delay_on_commit")
    def test_create_order(self, mock_send_sms, mock_mail_admin):
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

        # Verify that the order was created
        order = Order.objects.first()
        self.assertIsNotNone(order)
        self.assertEqual(order.customer.id, self.customer_x.id)

        # Verify that the SMS task was called with the correct arguments
        mock_send_sms.assert_called_once_with(
            "Your order has been placed.",
            [self.customer_x.phone_number],
        )

        # Verify that the email task was called with the correct arguments
        mock_mail_admin.assert_called_once_with(
            "New Order Placed.",
            f"Order ID: {order.id} \n Total Price: {order.total_price}",
        )

    @patch("shop.views.mail_admin.delay_on_commit")
    @patch("africas_talking.tasks.send_sms.delay_on_commit")
    def test_create_order_without_phone_number(self, mock_send_sms, mock_mail_admin):
        data = {
            "customer": self.customer_without_phone_number.id,
            "order_items": [{"product": self.product_x.id, "quantity": 4}],
        }
        response = self.client.post(self.list_endpoint, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data["customer"], self.customer_without_phone_number.id
        )
        self.assertEqual(
            response.data["order_items"][0]["product"]["id"], str(self.product_x.id)
        )
        self.assertEqual(response.data["order_items"][0]["quantity"], 4)

        # Verify that the order was created
        order = Order.objects.first()
        self.assertIsNotNone(order)
        self.assertEqual(order.customer.id, self.customer_without_phone_number.id)

        # Verify that the email task was called with the correct arguments
        mock_mail_admin.assert_called_once_with(
            "New Order Placed.",
            f"Order ID: {order.id} \n Total Price: {order.total_price}",
        )

        # Verify that the SMS task was not called
        mock_send_sms.assert_not_called()

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


class MailAdminTestCase(APITestCase):
    def test_mail_admin(self):
        # Without an admin
        result = mail_admin("Subject here", "Here is the message.")
        self.assertEqual(result, False)

        # With an admin
        get_user_model().objects.create_user(
            email="admin@test.com", password="password", is_admin=True
        )
        result = mail_admin("Subject here", "Here is the message.")
        self.assertEqual(result, True)
