from django.shortcuts import render, get_object_or_404, redirect
from .models import Booking, TeeTime
from django.contrib.auth.decorators import login_required
from .forms import TeeTimeForm
from datetime import datetime
from dateutil import parser
from django.utils import timezone
from django.contrib import messages
from django.urls import reverse


@login_required
def tee_time_booking(request):
    form = TeeTimeForm(request.POST or None, user=request.user)
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


@login_required
def booking_form(request, teetime_id):
    teetime = get_object_or_404(TeeTime, pk=teetime_id)
    form = TeeTimeForm(request.POST)

    return render(request, 'booking_form.html', {'teetime': teetime, 'form': form})


@login_required
def booking_submit(request):
    datetime_str = request.POST.get('date & time')
    players = request.POST.get('players')
    buggy = request.POST.get('buggy', False)
    if buggy == 'on':
        buggy = True
    else:
        buggy = False

    booking_datetime = timezone.make_aware(parser.parse(datetime_str))
    teetime = TeeTime.objects.get(tee_datetime=booking_datetime)

    new_booking = Booking(user_name=request.user, players=players,
                          booking_datetime=teetime, buggy=buggy)
    new_booking.save()

    messages.success(request, 'Booking created successfully!')

    # Get the booking ID (assuming your Booking model has an auto-generated primary key 'id')
    booking_id = new_booking.id

    # Redirect to the booking success page with the booking ID as a parameter
    return redirect('booking_success', booking_id=booking_id)


@ login_required
def booking_success(request, booking_id):

    context = {
        'booking_id': booking_id,
    }

    return render(request, 'booking_success.html', context)
