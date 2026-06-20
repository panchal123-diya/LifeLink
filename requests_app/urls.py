from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_request, name='create_request'),
    path('track/<uuid:token>/', views.track_request, name='track_request'),
    path('respond/<uuid:token>/', views.respond_request, name='respond_request'),
    
    path('create-bed/<int:hospital_id>/', views.create_bed_request, name='create_bed_request'),
    path('track-bed/<uuid:token>/', views.track_bed_request, name='track_bed_request'),
]
