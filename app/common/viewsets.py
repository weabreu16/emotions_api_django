from rest_framework import viewsets

class EagerModelViewSet(viewsets.ModelViewSet):
    """
    ModelViewSet that implement eager loading via serializer class
    that implement `EagerLoadingMixin`.
    """

    def get_queryset(self):
        queryset = super().get_queryset()
        serializer_class = self.get_serializer_class()
        
        if hasattr(serializer_class, 'setup_eager_loading'):
            queryset = serializer_class.setup_eager_loading(queryset)

        return queryset
