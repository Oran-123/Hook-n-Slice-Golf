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

    return render(request, 'user_profile.html', context)


def delete_booking(request):
    booking_id = request.POST.get('booking_id')
    if booking_id:
        booking = get_object_or_404(Booking, id=booking_id)
        booking.delete()
        messages.success(request, 'Booking deleted successfully.')
    else:
        messages.warning(request, 'Error deleting booking.')
    return redirect(request.META.get('HTTP_REFERER'))


def edit_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == 'POST':
        form = EditBooking(request.user, request.POST, instance=booking)
        if form.is_valid():
            form.save()
            messages.success(request, 'Booking editted successfully.')
            return redirect('user_profile_bookings')

    else:
        form = EditBooking(instance=booking)

    return render(request, 'edit_booking.html', {'form': form, 'booking_id': booking_id})


class ManageBookingListView(LoginRequiredMixin, UserPassesTestMixin, ListView):

    model = Booking
    template_name = 'manage_bookings.html'
    context_object_name = 'bookings'
    paginate_by = 10  # Number of bookings per page

    
    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context['paginator']
        page = self.request.GET.get('page')

        try:
            bookings = paginator.get_page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            bookings = paginator.get_page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            bookings = paginator.get_page(paginator.num_pages)

        context['bookings'] = bookings
        return context