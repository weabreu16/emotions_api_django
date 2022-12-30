from django.contrib import admin
from .models import Appointment

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['description', 'psychologist', 'patient', 'start', 'end', 'status', 'is_active', 'created_at']
    list_select_related = ['psychologist', 'patient']
    raw_id_fields = ['psychologist', 'patient']
    search_fields = [
        'psychologist__email', 
        'psychologist__first_name', 
        'psychologist__last_name',
        'patient__email', 
        'patient__first_name', 
        'patient__last_name',
    ]

admin.site.register(Appointment, AppointmentAdmin)
