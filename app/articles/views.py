from rest_framework.request import Request
from rest_framework.response import Response
from .models import Article
from .serializers import ArticleSerializer, GetArticleSerializer
from common.viewsets import EagerModelViewSet

class ArticleViewSet(EagerModelViewSet):
    queryset = Article.objects.all()
    http_method_names = ['get', 'post', 'retrieve', 'patch']

    def get_serializer_class(self):
        if hasattr(self, 'action') and self.action in ['list', 'retrieve']:
            return GetArticleSerializer
        return ArticleSerializer

    def list(self, request: Request, *args, **kwargs):
        query_params = request.query_params
        queryset = self.get_queryset().filter(is_active=True)

        psychologist = query_params.get('psychologist')
        if psychologist:
            queryset = queryset.filter(psychologist=psychologist)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
