from datetime import datetime
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from booking.models import Booking


@login_required
def user_profile_bookings(request):
    filter_type = request.POST.get('filter_type', 'upcoming')  # Default to 'upcoming' if no filter type is selected

    # Fetch the bookings based on the filter type
    if filter_type == 'past':
        bookings = Booking.objects.filter(user_name=request.user, booking_datetime__tee_datetime__lt=datetime.now()).order_by('-booking_datetime__tee_datetime')
        title = 'Past Bookings'
    else:
        bookings = Booking.objects.filter(user_name=request.user, booking_datetime__tee_datetime__gte=datetime.now()).order_by('booking_datetime__tee_datetime')
        title = 'Upcoming Bookings'

    context = {
        'bookings': bookings,
        'filter_type': filter_type,
        'title': title,
    }

    return render(request, 'user_profile.html', context)