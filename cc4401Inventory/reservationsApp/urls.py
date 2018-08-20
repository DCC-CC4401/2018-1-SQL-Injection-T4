from django.urls import path
from . import views

urlpatterns = [
    path('delete/', views.delete, name='delete_reservation'),
    path('reserve_sheet', views.reserve_sheet, name='reserve_sheet')
]
