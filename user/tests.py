from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient


class UserTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        User = get_user_model()

        users = [
            {"email": "usera@gmail.com", "password": "password"},
        ]

        self.client.force_authenticate(
            user=User.objects.create_user(email="userc@gmail.com", password="password")
        )

        for user in users:
            User.objects.create_user(**user)

        self.user_x = User.objects.create_user(
            email="userx@gmail.com", password="password"
        )

        self.list_endpoint = reverse("user_list")
        self.detail_endpoint = lambda id: reverse("user_detail", args=[id])

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

    def test_create_user(self):
        data = {"email": "userj@gmail.com", "password": "password"}
        response = self.client.post(self.list_endpoint, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["email"], "userj@gmail.com")

    def test_create_user_with_existing_email(self):
        data = {"email": "usera@gmail.com", "password": "password"}
        response = self.client.post(self.list_endpoint, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_user(self):
        endpoint = self.detail_endpoint(self.user_x.id)
        response = self.client.get(endpoint, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "userx@gmail.com")

    def test_get_users(self):
        endpoint = self.list_endpoint
        response = self.client.get(endpoint, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user(self):
        endpoint = self.detail_endpoint(self.user_x.id)
        response = self.client.put(endpoint, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "userx@gmail.com")

    def test_delete_user(self):
        user_y = get_user_model().objects.create_user(
            email="usery@gmail.com", password="password"
        )
        endpoint = self.detail_endpoint(user_y.id)
        response = self.client.delete(endpoint, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(get_user_model().objects.filter(id=user_y.id).count(), 0)

    def test_current_user(self):
        response = self.client.get(reverse("user_me"), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "userc@gmail.com")

    def test_create_super_user(self):
        super_user = get_user_model().objects.create_superuser(
            email="superuser@gmail.com", password="password"
        )
        self.assertEqual(super_user.is_superuser, True)
        self.assertEqual(super_user.is_staff, True)
        self.assertEqual(super_user.is_admin, True)
        self.assertEqual(super_user.email, "superuser@gmail.com")

    def test_create_user_without_email(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email=None, password="password")

    def test_user_model_str_dunder_method(self):
        user = get_user_model().objects.create_user(
            email="userz@gmail.com", password="password"
        )
        self.assertEqual(str(user), "userz@gmail.com")
