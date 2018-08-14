from django.contrib import admin
from .models import Loan


class LoanAdministrator(admin.ModelAdmin):
    list_display = ('id', 'user_full_name', 'article_name', 'starting_date_time', 'ending_date_time', 'state')

    @staticmethod
    def user_full_name(loan):
        return loan.user.get_full_name()

    @staticmethod
    def article_name(loan):
        return loan.article.name


admin.site.register(Loan, LoanAdministrator)
