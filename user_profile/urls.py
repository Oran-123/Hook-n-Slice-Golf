from django.urls import path
from user_profile.views import user_profile_bookings, edit_booking, ManageBookingListView, admin_delete_booking


urlpatterns = [

    path('', user_profile_bookings, name='user_profile_bookings'),
    path('edit_booking/<int:booking_id>/', edit_booking, name='edit_booking'),
    path('manage-bookings/', ManageBookingListView.as_view(),
         name='ManageBookingListView'),
    path('admin-delete-booking/', ManageBookingListView.as_view(admin_delete_booking),
         name='admin_delete_booking'),



]
