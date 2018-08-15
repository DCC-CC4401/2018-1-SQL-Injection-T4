from django.contrib import admin
from .models import User


class UserAdministrator(admin.ModelAdmin):
    list_display = ('id', 'email', 'first_name', 'last_name', 'rut', 'is_active', 'is_staff', 'date_joined', 'last_login')


admin.site.register(User, UserAdministrator)
