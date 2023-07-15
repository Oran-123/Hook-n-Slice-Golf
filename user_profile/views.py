from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from booking.models import Booking
from django.shortcuts import get_object_or_404
from .forms import EditBooking
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


@login_required
def user_profile_bookings(request):
    # Default to 'upcoming' if no filter type is selected
    filter_type = request.POST.get('filter_type', 'upcoming')

    # Fetch the bookings based on the filter type
    if filter_type == 'past':
        bookings = Booking.objects.filter(user_name=request.user, booking_datetime__tee_datetime__lt=datetime.now(
        )).order_by('-booking_datetime__tee_datetime')
        title = 'Past Bookings'
    else:
        bookings = Booking.objects.filter(user_name=request.user, booking_datetime__tee_datetime__gte=datetime.now(
        )).order_by('booking_datetime__tee_datetime')
        title = 'Upcoming Bookings'

    context = {
        'bookings': bookings,
        'filter_type': filter_type,
        'title': title,
    }

    if request.method == 'POST':
        get_booking_id(request)

    return render(request, 'user_profile.html', context)


def get_booking_id(request):
    booking_id = request.POST.get('booking_id')
    if booking_id:
        delete_booking(booking_id)


def delete_booking(booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.delete()


def edit_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == 'POST':
        form = EditBooking(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            return redirect('user_profile_bookings')
    else:
        form = EditBooking(instance=booking)

    return render(request, 'edit_booking.html', {'form': form, 'booking_id': booking_id})


class ManageBookingListView(LoginRequiredMixin, UserPassesTestMixin, ListView):

    model = Booking
    template_name = 'manage_bookings.html'
    context_object_name = 'bookings'

    def test_func(self):
        return self.request.user.is_superuser

    def admin_delete_booking(self):
        if request.method == 'POST':
            get_booking_id(request)
