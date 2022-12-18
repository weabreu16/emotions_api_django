from django.contrib.auth.hashers import make_password, check_password
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, AuthSerializer
from .models import User
from .authentication import EmotionsJWTAuthentication

class UserViewSet(viewsets.ModelViewSet):
    """
    View for list, create, update and delete users.
    """
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

class AuthViewSet(viewsets.GenericViewSet):
    """
    View that validate user login data and generate a JWTToken.
    """
    queryset = User.objects.all()
    serializer_class = AuthSerializer

    def generate_token(self, user):
        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def login(self, user_auth):
        user = self.get_queryset().filter(email=user_auth['email']).first()

        if not user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if not check_password(user_auth['password'], user.password):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        tokens = self.generate_token(user)
        return Response(tokens, status.HTTP_201_CREATED)

    def create(self, request: Request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return self.login(serializer.data)

    @action(detail=False, methods=['post'])
    def refresh(self, request: Request):
        serializer = TokenRefreshSerializer()
        token = serializer.validate(request.data)
        return Response(token)
