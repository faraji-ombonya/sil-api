from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from user import views


urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("users/", views.UserList.as_view(), name="user_list"),
    path("users/me/", views.UserMe.as_view(), name="user_me"),
    path("users/<uuid:pk>/", views.UserDetail.as_view(), name="user_detail"),
]
