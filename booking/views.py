from django.shortcuts import render
from django.views import generic
from .models import TeeTime

# Create your views here.

def booking (request):
    return render(request, "templates/booking.html") 
