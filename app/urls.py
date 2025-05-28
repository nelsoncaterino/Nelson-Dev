from django.urls import path, include 
from . import views
from app.views import home, services, about, contact

urlpatterns = [
    path('', home, name='home'),
    path('services/', services, name='services'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
]
