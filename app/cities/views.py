from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import City
from .serializers import CitySerializer

class CityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_active']
