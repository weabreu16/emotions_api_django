from django.contrib.auth.hashers import make_password
from rest_framework import status, viewsets
from rest_framework.response import Response
from .serializers import UserSerializer
from .models import User

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        users = self.get_queryset().filter(is_active=True)
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        user = request.data

        if user.get('password'):
            user['password'] = make_password(user['password'])

        serializer = self.get_serializer(data=user)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)