from django.db import models
from users.models import User

class AppointmentStatus(models.TextChoices):
    SCHEDULED = 'Scheduled',
    STARTED = 'Started',
    COMPLETED = 'Completed',
    REFERRED = 'Referred'

class Appointment(models.Model):
    description = models.CharField(max_length=255, null=True)
    start = models.DateTimeField()
    end = models.DateTimeField()
    psychologist = models.ForeignKey(User, on_delete=models.CASCADE, related_name="appointment_psychologist")
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="appointment_patient")
    status = models.TextField(choices=AppointmentStatus.choices, default=AppointmentStatus.SCHEDULED)
    started = models.DateTimeField(null=True)
    completed = models.DateTimeField(null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
