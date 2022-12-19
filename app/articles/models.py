from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=50)
    body = models.TextField()
    psychologist = models.ForeignKey('users.User', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
