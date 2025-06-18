from django.shortcuts import render
from django.http import HttpResponse
from django.urls import path, include

# Create your views here.
def home(request):
    return render(request, 'home.html')

def services(request):
    return render(request, 'services.html')

def about(request):
    return render(request, 'about.html', )

def contact(request):
    return render(request, 'contact.html')

