from django.contrib.auth.hashers import make_password
from rest_framework import status, viewsets
from rest_framework.response import Response
from .serializers import UserSerializer
from .models import User

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def pre_save(self, request):
        if request.data['password']:
            request.data['password'] = make_password(request.data['password'])
        return request

    def list(self, request, *args, **kwargs):
        users = self.get_queryset().filter(is_active=True)
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        request = self.pre_save(request)
        return super().create(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        request = self.pre_save(request)
        return super().partial_update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if request.method == "PUT":
            return Response(None, status.HTTP_405_METHOD_NOT_ALLOWED)

        return super().update(request, *args, **kwargs)
