from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('hospitals/', views.hospital_search, name='hospital_search'),
    path('hospital/<int:pk>/', views.hospital_detail, name='hospital_detail'),
    path('bloodbanks/', views.bloodbank_search, name='bloodbank_search'),
    path('sos/', views.sos_page, name='sos'),
]
