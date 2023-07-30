"""
Booking App - form
---------------------
Form for booking app

"""
# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from django import forms
from django.forms.widgets import CheckboxSelectMultiple
from .models import Booking, TeeTime
from django.contrib import messages
from datetime import date, datetime, time
from django.utils import timezone
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class TeeTimeForm(forms.Form):

    """
    Form that enables users to enter their booking criteria and return
    available teetimes
    """

    def __init__(self, *args, user=None, **kwargs):
        """
        Initialize form with optional user data. Set 'user' attribute and
        field initial values.
        """
        self.user = user
        super().__init__(*args, **kwargs)
        self.fields['date'].initial = date.today()
        self.fields['players'].initial = 1

    date = forms.DateField(widget=forms.DateInput(
        attrs={'class': 'form-control', 'type': 'date',
               'min': datetime.today().date()}))
    start_time = forms.TimeField(widget=forms.TimeInput(
        attrs={'class': 'form-control', 'type': 'time', }))
    end_time = forms.TimeField(widget=forms.TimeInput(
        attrs={'class': 'form-control', 'type': 'time', }))
    players = forms.IntegerField(widget=forms.NumberInput(
        attrs={'class': 'form-control', 'min': '1', 'max': '4'}))

    def clean(self):
        """
        Clean and validate form data. Check for existing bookings,
        time constraints, and errors.
        """
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        today = date.today()
        time_now = datetime.now().time()

        if date:
            # Query for any existing bookings for the same date and user
            existing_booking = Booking.objects.filter(
                user_name=self.user,
                booking_datetime__tee_datetime__date=date
            ).first()

            if existing_booking:
                self.add_error(
                    None, f"""You have already booked a tee time on {date}.
                    You are only permitted to make one booking per day.""")

        if date == today and start_time < time_now:
            formatted_start_time = start_time.strftime('%H:%M')
            formatted_time_now = time_now.strftime('%H:%M')
            self.add_error(
                None, f"""You're selected start time {formatted_start_time} is
                in the past please try again and select a start time
                after {formatted_time_now}.""")

        if start_time and end_time and start_time >= end_time:
            self.add_error(
                'end_time', 'End time must be later than start time.')

    def get_available_tee_times(self):
        """
        Get available tee times based on cleaned form data.
        Query and filter TeeTime objects.
        """

        date = self.cleaned_data.get('date')
        start_time = self.cleaned_data.get('start_time')
        end_time = self.cleaned_data.get('end_time')
        players = self.cleaned_data.get('players')

        tee_times = TeeTime.objects.filter(
            tee_datetime__date=date,
            tee_datetime__time__gte=start_time,
            tee_datetime__time__lte=end_time,
            max_players__gte=players,
            available=True
        ).order_by('tee_datetime')

        for tee_time in tee_times:
            tee_time.num_booked_players = tee_time.available_slots()

        return tee_times
