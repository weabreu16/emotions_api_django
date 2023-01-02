from django.contrib import admin
from .models import City

class CityAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at']
    search_fields = ['name']

admin.site.register(City, CityAdmin)
