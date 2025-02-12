from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from user.serializers import CreateUserSerializer, UserSerializer
from user.models import User
from utils.pagination import StandardPagination
from utils.open_api import get_paginated_response_schema, page, per_page


class AuthenticatedAPIView(APIView):
    permission_classes = [IsAuthenticated]


@extend_schema(tags=["User"])
@extend_schema_view(
    get=extend_schema(
        parameters=[page, per_page],
        responses={
            200: get_paginated_response_schema(
                UserSerializer, "Paginated list of users"
            ),
        },
    ),
)
class UserList(AuthenticatedAPIView):
    serializer_class = CreateUserSerializer
    pagination_class = StandardPagination

    def get(self, request, format=None):
        paginator = self.pagination_class()
        users = paginator.paginate_queryset(User.objects.all(), request)
        serializer = UserSerializer(users, many=True)
        response = paginator.get_paginated_response(serializer.data)
        return Response(response, status=200)

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)


@extend_schema(tags=["User"])
@extend_schema_view(put=extend_schema(request=CreateUserSerializer))
class UserDetail(AuthenticatedAPIView):
    serializer_class = UserSerializer

    def get(self, request, pk, format=None):
        user = get_object_or_404(User, pk=pk)
        serializer = self.serializer_class(user)
        return Response(serializer.data, status=200)

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
