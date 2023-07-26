from django import forms
from booking.models import Booking, TeeTime
from django.utils import timezone
from datetime import date


class EditBooking(forms.ModelForm):

    class Meta:
        model = Booking
        fields = ['booking_date', 'booking_time', 'players', 'buggy']
        widgets = {
            'players': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '4'}),
            'buggy': forms.CheckboxInput(attrs={'class': 'form-check-input'})
            'booking_date'forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'min': datetime.today().date()})
            'booking_time'forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'})
        }


def combine_booking_date_time(self):
    cleaned_data = super().clean()
    booking_date = cleaned_data.get('booking_date')
    booking_time = cleaned_data.get('booking_time')

    if booking_date and booking_time:
        cleaned_data['booking_datetime'] = timezone.make_aware(
            timezone.datetime.combine(booking_date, booking_time)
        )

    return cleaned_data
