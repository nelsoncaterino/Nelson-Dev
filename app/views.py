from django.shortcuts import render
from django.http import HttpResponse
from django.urls import path, include

# Create your views here.
def home(request):
    return render(request, 'home.html')

def services(request):
    return render(request, 'services.html')

def about(request):
    context = {
        'text': [{'content': 'lorem ipsum.'}],
        'photo': [
            {'image_url': 'img/1627469713006.jpeg', 'caption': 'Photo 1', 'z_index': 1},
            {'image_url': 'img/capture_ecran_2025_02_26_091907.png', 'caption': 'Photo 2', 'z_index': 1},
            {'image_url': 'img/IMG20240113134449.PNG', 'caption': 'Photo 3', 'z_index': 1},
            {'image_url': 'img/raki.jpg', 'caption': 'Photo 4', 'z_index': 1},
        ],
    }
    return render(request, 'about.html', context)
def contact(request):
    return render(request, 'contact.html')
