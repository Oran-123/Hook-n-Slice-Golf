"""
User Profile App - URLs
---------------------
URLs for User Profile App

"""
# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from django.urls import path
from user_profile.views import (
    user_profile_bookings,
    edit_booking, ManageBookingListView,
    delete_booking,
    generate_tee_times,
)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


urlpatterns = [

    path('', user_profile_bookings, name='user_profile_bookings'),
    path('edit_booking/<int:booking_id>/', edit_booking, name='edit_booking'),
    path('delete_booking/', delete_booking, name='delete_booking'),
    path('manage-bookings/', ManageBookingListView.as_view(),
         name='ManageBookingListView'),
    path('generate-tee-times/', generate_tee_times,
         name='generate_tee_times'),
]
