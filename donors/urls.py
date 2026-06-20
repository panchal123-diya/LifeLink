from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.donor_dashboard, name='donor_dashboard'),
]
