from django.contrib import admin
from .models import TeeTime, Booking

# Register your models here.

admin.site.register(TeeTime, Booking)
