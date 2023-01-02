from django.utils.timezone import datetime
from django.db.models import Q, QuerySet
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from common.viewsets import EagerModelViewSet
from common.helpers import get_param
from .models import Appointment
from .serializers import GetAppointmentSerializer, AppointmentSerializer

class AppointmentViewSet(EagerModelViewSet):
    queryset = Appointment.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if hasattr(self, 'action') and self.action in ['list', 'retrieve']:
            return GetAppointmentSerializer
        return AppointmentSerializer

    def validate_collisions(self, appointment) -> bool:

        queryset = self.get_queryset().filter(
            start__lt=appointment.get("end"),
            end__gt=appointment.get("start"),
            is_active=True
        )

        appointment_id = appointment.get("id")
        if appointment_id:
            queryset = queryset.filter(~Q(id=appointment_id))

        return bool(len(queryset))

    def list(self, request: Request, *args, **kwargs):
        query_params = request.query_params

        userId = get_param(query_params, "userId", cast=int)
        date = get_param(query_params, "date", cast=datetime.fromisoformat)
        status = get_param(query_params, "status", default=None, raise_exception=False)

        queryset: QuerySet = self.get_queryset().filter(
            Q(psychologist=userId) | Q(patient=userId),
            start__year=date.year, start__month=date.month, start__day=date.day,
            is_active=True
        ).order_by("-start")

        if status:
            queryset = queryset.filter(status=status)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request: Request, *args, **kwargs):
        serializer: AppointmentSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if self.validate_collisions(serializer.validated_data):
            return Response("The appointment is colliding with the date", status=status.HTTP_409_CONFLICT)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request: Request, *args, **kwargs):
        instance: Appointment = self.get_object()
        serializer: AppointmentSerializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        if self.validate_collisions(instance.__dict__ | serializer.validated_data):
            return Response("The appointment is colliding with the date", status=status.HTTP_409_CONFLICT)

        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
