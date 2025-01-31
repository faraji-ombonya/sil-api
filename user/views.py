from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from user.serializers import (
    CreateUserSerializer,
    UserSerializer,
    UserPaginationSerializer,
)
from user.models import User
from utils.pagination import StandardPagination


class AuthenticatedAPIView(APIView):
    permission_classes = [IsAuthenticated]


@extend_schema(tags=["User"])
class UserList(AuthenticatedAPIView):
    serializer_class = CreateUserSerializer
    pagination_class = StandardPagination

    @extend_schema(responses={200: UserPaginationSerializer})
    def get(self, request, format=None):
        paginator = self.pagination_class()
        users = paginator.paginate_queryset(User.objects.all(), request)
        serializer = UserSerializer(users, many=True)
        response = paginator.get_paginated_response(serializer.data)
        return Response(response, status=200)

    @extend_schema(responses={201: UserSerializer})
    def post(self, request, format=None):
        serializer = CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)


@extend_schema(tags=["User"])
class UserDetail(AuthenticatedAPIView):
    serializer_class = UserSerializer

    def get(self, request, pk, format=None):
        user = get_object_or_404(User, pk=pk)
        serializer = self.serializer_class(user)
        return Response(serializer.data, status=200)

    @extend_schema(request=CreateUserSerializer)
    def put(self, request, pk, format=None):
        user = get_object_or_404(User, pk=pk)
        serializer = CreateUserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)

    def delete(self, request, pk, format=None):
        user = get_object_or_404(User, pk=pk)
        user.delete()
        return Response(status=204)


@extend_schema(tags=["User"])
class UserMe(AuthenticatedAPIView):
    serializer_class = UserSerializer

    def get(self, request, format=None):
        user = request.user
        serializer = self.serializer_class(user)
        return Response(serializer.data, status=200)
