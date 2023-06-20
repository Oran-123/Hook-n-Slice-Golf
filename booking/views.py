from django.shortcuts import render, get_object_or_404, redirect
from .models import Booking, TeeTime
from django.contrib.auth.decorators import login_required
from .forms import TeeTimeForm


@login_required
def tee_time_booking(request):
    form = TeeTimeForm(request.POST or None)
    available_tee_times = []

    if request.method == 'POST' and form.is_valid():
        available_tee_times = form.get_available_tee_times()

    context = {
        'form': form,
        'available_tee_times': available_tee_times
    }

    return render(request, 'booking.html', context)