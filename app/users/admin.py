from django.contrib import admin
from .forms import User, UserForm

class UserAdmin(admin.ModelAdmin):
    form = UserForm

admin.site.register(User, UserAdmin)
