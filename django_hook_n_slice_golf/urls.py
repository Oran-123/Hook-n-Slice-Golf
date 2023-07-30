
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

handler404 = 'home.views.custom_404_view'
handler403 = 'home.views.custom_403_view'
handler500 = 'home.views.custom_500_view'
