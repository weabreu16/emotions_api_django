from django.contrib import admin
from .forms import User, UserForm

class UserAdmin(admin.ModelAdmin):
    form = UserForm
    list_display = ['email', 'first_name', 'last_name', 'is_active', 'created_at']
    search_fields = ['email', 'first_name', 'last_name']

admin.site.register(User, UserAdmin)
