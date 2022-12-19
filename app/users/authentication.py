from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed, InvalidToken
from rest_framework_simplejwt.settings import api_settings
from .models import User

class EmotionsJWTAuthentication(JWTAuthentication):
    """
    Implementation of JWTAuthentication from Simple JWT 
    using Custom User (not Django default).
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_model = User

    def authenticate(self, request):
        result = super().authenticate(request)
        
        if not result:
            raise InvalidToken("Token contained no recognizable user identification")

        return result

    def get_user(self, validated_token):
        try:
            user_id = validated_token[api_settings.USER_ID_CLAIM]
        except KeyError:
            raise InvalidToken("Token contained no recognizable user identification")

        try:
            user = self.user_model.objects.get(**{api_settings.USER_ID_FIELD: user_id})
        except self.user_model.DoesNotExist:
            raise AuthenticationFailed("User not found", code="user_not_found")

        if not user.is_active:
            raise AuthenticationFailed("User is inactive", code="user_inactive")

        return user

    
