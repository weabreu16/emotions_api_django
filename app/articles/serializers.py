from rest_framework import serializers
from .models import Article
from users.models import User
from users.serializers import UserSerializer
from common.mixins import EagerLoadingMixin

class GetArticleSerializer(EagerLoadingMixin, serializers.ModelSerializer):
    psychologist = UserSerializer()
    select_related_fields = ['psychologist']

    class Meta:
        model = Article
        fields = '__all__'

class ArticleSerializer(serializers.ModelSerializer):
    psychologist = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Article
        fields = '__all__'
