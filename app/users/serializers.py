from rest_framework import serializers
from .models import Note, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class AuthSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class NoteSerializer(serializers.ModelSerializer):
    psychologist = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    patient = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Note
        fields = '__all__'
