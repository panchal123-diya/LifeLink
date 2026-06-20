from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.hospital_dashboard, name='hospital_dashboard'),
    path('respond-bed/<int:request_id>/', views.respond_bed_request, name='respond_bed_request'),
]
