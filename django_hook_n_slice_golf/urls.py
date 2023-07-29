"""django_hook_n_slice_golf URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from booking.views import tee_time_booking, booking_form, booking_submit
from home.views import custom_404_view, custom_403_view, custom_500_view
from django.conf.urls import handler404, handler403, handler500



urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('booking/',  include('booking.urls'), name='booking-urls'),
    path('', include('home.urls'), name='home-urls'),
    path('user/',  include('user_profile.urls'), name='user-profile-urls'),


]

handler404 = custom_404_view
handler403 = custom_403_view
handler500 = custom_500_view

