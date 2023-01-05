from typing import List, Dict

from django.utils.timezone import datetime
from django.db.models import Q, QuerySet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.request import Request
from rest_framework.response import Response

from common.viewsets import EagerModelViewSet
from common.helpers import get_param
from .models import Appointment
from .serializers import GetAppointmentSerializer, AppointmentSerializer

AppointmentHistory = Dict[str, List[Dict]]

class AppointmentViewSet(EagerModelViewSet):
    queryset = Appointment.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        if hasattr(self, 'action') and self.action in ['list', 'retrieve', 'history']:
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

    @action(methods=["get"], detail=False)
    def history(self, request: Request, *args, **kwargs):
        userId: str = get_param(request.query_params, "userId")

        queryset = self.get_queryset() \
            .filter(
                Q(psychologist=userId) | Q(patient=userId),
                status="Completed",
                is_active=True
            ) \
            .order_by("-start")

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            history = self.create_history(serializer.data)
            return self.get_paginated_response(history)

        serializer = self.get_serializer(queryset, many=True)
        history = self.create_history(serializer.data)
        return Response(history)

    def create_history(self, appointments: List[Dict]) -> List[AppointmentHistory]:
        
        appointment_histories = []

        appointment_history_by_date: AppointmentHistory = dict()

        for appointment in appointments:
            date: datetime = datetime.fromisoformat(appointment["start"])
            formatted_date = f"{date.year}-{date.month}-{date.day}"

            if appointment_history_by_date.get(formatted_date):
                appointment_history_by_date[formatted_date].append(appointment)
            else:
                appointment_history_by_date[formatted_date] = [appointment]

        for key, val in appointment_history_by_date.items():
            appointment_histories.append({"date": key, "appointments": val})

        return appointment_histories
