from rest_framework import serializers
from .models import Article

class ArticleSerializer(serializers.ModelSerializer):
    psychologist = serializers.PrimaryKeyRelatedField()

    class Meta:
        model = Article
        fields = '__all__'
