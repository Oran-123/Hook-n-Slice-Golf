"""
Booking App - urls
---------------------
Urls for booking app

"""
# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from django.urls import path
from booking.views import tee_time_booking, booking_form, booking_submit
from . import views
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


urlpatterns = [

    path('createbooking', tee_time_booking, name='tee_time_booking'),
    path('<int:teetime_id>', booking_form, name='booking_form'),
    path('submit/', booking_submit, name='booking_submit'),
    path('booking/booking_success/<int:booking_id>',
         views.booking_success, name='booking_success'),

]
