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

        players = form.cleaned_data.get('players')

        # Filter out tee times that don't have enough available slots
        available_tee_times = [
            tee_time for tee_time in available_tee_times if tee_time.available_slots() >= players]

    context = {
        'form': form,
        'available_tee_times': available_tee_times
    }

    return render(request, 'booking.html', context)