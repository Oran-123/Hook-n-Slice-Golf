from django.shortcuts import render, get_object_or_404, redirect
from .models import Booking, TeeTime
from django.contrib.auth.decorators import login_required
from .forms import TeeTimeForm
from datetime import datetime
from dateutil import parser


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


@login_required
def booking_form(request, teetime_id):
    teetime = get_object_or_404(TeeTime, pk=teetime_id)
    form = TeeTimeForm(request.POST)

    return render(request, 'booking_form.html', {'teetime': teetime, 'form': form})


@login_required
def booking_submit(request):

    if request.method == 'POST':
        datetime_str = request.POST.get('date & time')
        players = request.POST.get('players')
        buggy = request.POST.get('buggy', False)
        # Convert buggy value to a boolean
        if buggy == 'on':
            buggy = True
        else:
            buggy = False 

        booking_datetime = parser.parse(datetime_str)
        teetime = TeeTime.objects.get(tee_datetime=booking_datetime)


        # Process the form data and create the booking
        Booking(user_name=request.user, players=players,
                          booking_datetime=teetime, buggy=buggy).save()

        # Redirect the user to the booking success page or any other relevant view
        return redirect('booking.html')
        print(Booking)

    return render(request, 'booking.html')


