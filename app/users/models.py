from django.db import models

class User(models.Model):
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=255)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Note(models.Model):
    psychologist = models.ForeignKey(User, on_delete=models.CASCADE, primary_key=True, related_name="psychologist")
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="patient")
    note = models.TextField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['psychologist','patient'], name="unique_psychologist_patient")
        ]
