from django.contrib.auth.hashers import make_password, check_password
from rest_framework import status, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import AuthSerializer, NoteSerializer, UserSerializer
from .models import Note, User
from .authentication import EmotionsJWTAuthentication
from common.helpers import get_param

class UserViewSet(viewsets.ModelViewSet):
    """
    View for list, create, update and delete users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [EmotionsJWTAuthentication]

    def pre_save(self, request):
        if request.data['password']:
            request.data['password'] = make_password(request.data['password'])
        return request

    def perform_authentication(self, request: Request):
        if request.method == "POST":
            return

        main_authenticator = self.get_authenticators()[0]
        main_authenticator.authenticate(request)

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

class NoteViewSet(viewsets.GenericViewSet, 
        mixins.CreateModelMixin, 
        mixins.UpdateModelMixin
    ):
    """
    View for retrieve, create and update psychologist notes associated with a patient.
    """
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    http_method_names = ["get", "post", "patch"]
    
    def get_note(self, request: Request):
        query_params = request.query_params
        psychologist = get_param(query_params, 'psychologist')
        patient = get_param(query_params, 'patient')

        note = self.get_queryset().filter(psychologist=psychologist, patient=patient).first()

        serializer = self.get_serializer(note)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        return self.get_note(request)
