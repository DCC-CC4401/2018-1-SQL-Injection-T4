from django.urls import path
from . import views

urlpatterns = [
    path('lost_article/', views.lost_article, name='lost_article'),
]