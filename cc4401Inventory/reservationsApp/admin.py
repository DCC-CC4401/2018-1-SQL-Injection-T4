from django.contrib import admin
from .models import Reservation


class ReservationAdministrator(admin.ModelAdmin):
    list_display = ('id', 'user_full_name', 'space_name', 'starting_date_time', 'ending_date_time', 'state')

    @staticmethod
    def user_full_name(loan):
        return loan.user.get_full_name()

    @staticmethod
    def space_name(loan):
        return loan.space.name


admin.site.register(Reservation, ReservationAdministrator)
