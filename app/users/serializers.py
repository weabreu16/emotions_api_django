from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class AuthSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
