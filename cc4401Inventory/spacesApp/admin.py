from django.contrib import admin
from .models import Space


class SpaceAdministrator(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'state')


admin.site.register(Space, SpaceAdministrator)
