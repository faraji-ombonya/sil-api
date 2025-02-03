from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase, APIClient


class UserTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        User = get_user_model()

        users = [
            {"email": "usera@gmail.com", "password": "password"},
        ]

        for user in users:
            User.objects.create_user(**user)

    def test_login_user(self):
        endpoint = "/v1/user/token/"

        data = {
            "email": "usera@gmail.com",
            "password": "password",
        }

        response = self.client.post(endpoint, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
