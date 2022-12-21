from rest_framework import serializers
from .models import Article
from users.models import User
from users.serializers import UserSerializer

class GetArticleSerializer(serializers.ModelSerializer):
    psychologist = UserSerializer()

    class Meta:
        model = Article
        fields = '__all__'

class ArticleSerializer(serializers.ModelSerializer):
    psychologist = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Article
        fields = '__all__'
