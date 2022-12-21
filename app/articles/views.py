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
