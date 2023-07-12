from django.urls import path
from user_profile.views import user_profile_bookings


urlpatterns = [

    path('', user_profile_bookings, name='user_profile_bookings'),
]
