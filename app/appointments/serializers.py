from rest_framework import serializers
from common.mixins import EagerLoadingMixin
from users.serializers import UserSerializer
from users.models import User
from .models import Appointment
from .validators import DateRangeValidator

class GetAppointmentSerializer(EagerLoadingMixin, serializers.ModelSerializer):
    psychologist = UserSerializer()
    patient = UserSerializer()
    select_related_fields = ['psychologist', 'patient']

    class Meta:
        model = Appointment
        fields = '__all__'

class AppointmentSerializer(serializers.ModelSerializer):
    psychologist = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    patient = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Appointment
        fields = '__all__'
        validators = [
            DateRangeValidator(start_date_field="start", end_date_field="end")
        ]
