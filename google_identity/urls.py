from django.urls import path

from . import views


urlpatterns = [
    path("signin-page/", views.ServerFlowSignIn.as_view(), name="signin_page"),
    path(
        "signin-callback/", views.ServerFlowCallback.as_view(), name="signin_callback"
    ),
]
