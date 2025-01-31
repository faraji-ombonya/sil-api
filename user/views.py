from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from user.serializers import CreateUserSerializer, UserSerializer
from user.models import User


class AuthenticatedAPIView(APIView):
    permission_classes = [IsAuthenticated]


class UserList(APIView):
    def get(self, request, format=None):
        page = request.GET.get("page", 1)
        per_page = request.GET.get("per_page", 10)
        offset = (int(page) - 1) * int(per_page)
        limit = offset + int(per_page)
        users = User.objects.all()
        count = users.count()
        serializer = CreateUserSerializer(users[offset:limit], many=True)
        response = {
            "page": page,
            "per_page": per_page,
            "count": count,
            "results": serializer.data,
        }
        return Response(response, status=200)

    def post(self, request, format=None):
        serializer = CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)


class UserDetail(APIView):
    def get(self, request, pk, format=None):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user)
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


class UserMe(AuthenticatedAPIView):
    def get(self, request, format=None):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=200)
