"""
User Profile App - Views
---------------------
Views for User Profile App

"""
# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from booking.models import Booking
from django.shortcuts import get_object_or_404
from .forms import EditBooking
from django.views.generic import ListView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage
from django.contrib.auth.decorators import user_passes_test
from booking.models import TeeTime
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


@login_required
def user_profile_bookings(request):
    """
    Render user profile bookings based on the 'filter_type' parameter.
    """
    # Default to 'upcoming' if no filter type is selected
    filter_type = request.POST.get('filter_type', 'upcoming')
    # Fetch the bookings based on the filter type
    if filter_type == 'past':
        bookings = (
            Booking.objects.filter(
                user_name=request.user,
                booking_datetime__tee_datetime__lt=datetime.now()
            ).order_by('-booking_datetime__tee_datetime')
        )

        title = 'Past Bookings'
    else:
        bookings = (
            Booking.objects.filter(
                user_name=request.user,
                booking_datetime__tee_datetime__gte=datetime.now()
            ).order_by('booking_datetime__tee_datetime')
        )
        title = 'Upcoming Bookings'

    context = {
        'bookings': bookings,
        'filter_type': filter_type,
        'title': title,
    }

    return render(request, 'user_profile.html', context)


def delete_booking(request):
    """
    Delete a booking based on the 'booking_id' passed in POST parameters.
    """
    booking_id = request.POST.get('booking_id')
    if booking_id:
        booking = get_object_or_404(Booking, id=booking_id)
        booking.delete()
        messages.success(request, 'Booking deleted successfully.')
    else:
        messages.warning(request, 'Error deleting booking.')
    return redirect(request.META.get('HTTP_REFERER'))


def edit_booking(request, booking_id):
    """
    Edit a booking with the given 'booking_id' and handle form submission.
    """
    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == 'POST':
        form = EditBooking(request.user, request.POST, instance=booking)
        if form.is_valid():
            form.save()
            messages.success(request, 'Booking editted successfully.')
            return redirect('user_profile_bookings')

    else:
        form = EditBooking(instance=booking)

    return render(request, 'edit_booking.html',
                  {'form': form, 'booking_id': booking_id})


@user_passes_test(lambda u: u.is_superuser)
def generate_tee_times(request):
    """
    View to trigger the creation of tee times by the superuser.
    """
    TeeTime.create_tee_times()
    messages.success(request, 'Tee times have been successfully generated!')
    return redirect(request.META.get('HTTP_REFERER'))


class ManageBookingListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """
    Edit a booking with the given 'booking_id' and handle form submission.
    """
    model = Booking
    template_name = 'manage_bookings.html'
    context_object_name = 'bookings'
    paginate_by = 10

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context['paginator']
        page = self.request.GET.get('page')

        try:
            bookings = paginator.get_page(page)
        except PageNotAnInteger:
            bookings = paginator.get_page(1)
        except EmptyPage:
            bookings = paginator.get_page(paginator.num_pages)

        context['bookings'] = bookings
        return context
