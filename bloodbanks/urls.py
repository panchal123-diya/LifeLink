from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.bloodbank_dashboard, name='bloodbank_dashboard'),
]
