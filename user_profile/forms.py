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

