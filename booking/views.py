from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from .models import Booking, TeeTime
from django.contrib.auth.decorators import login_required
from datetime import datetime



@login_required
def select_date(request):
    if request.method == 'POST':
        selected_date = request.POST.get('selected_day')
        teetimes = TeeTime.objects.filter(tee_datetime__date=selected_date)
        return render(request, 'booking.html', {'teetimes': teetimes})
    else:
        return render(request, 'booking.html')

@login_required
def book_teetime(request, teetime_id):
    teetime = get_object_or_404(TeeTime, id=teetime_id)
    if request.method == 'POST':
        players = int(request.POST.get('players', 1))
        buggy = request.POST.get('buggy', False)

        # Combine selected date and time into a single datetime value
        selected_date = datetime.strptime(
            request.POST.get('selected_date'), '%Y-%m-%d').date()
        selected_time = datetime.strptime(
            request.POST.get('selected_time'), '%H:%M').time()
        tee_datetime = datetime.combine(selected_date, selected_time)

        if players > teetime.available_slots():
            error_message = f"You are trying to make a booking for {players} players, but this tee time only has space for {teetime.available_slots()} players."
            return render(request, 'booking.html', {'teetime': teetime, 'error_message': error_message})

        booking_datetime = TeeTime.objects.get(tee_datetime=tee_datetime)

        booking = Booking.objects.create(
            user_name=request.user, players=players, booking_datetime=booking_datetime, buggy=buggy)
        booking.save()
        return redirect('confirmation')
    else:
        return render(request, 'booking.html', {'teetime': teetime})
