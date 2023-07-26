from django import forms
from booking.models import Booking, TeeTime
from django.utils import timezone


class EditBooking(forms.ModelForm):
    
    class Meta:
        model = Booking
        fields = ['booking_date','booking_time', 'players', 'buggy']
        widgets = {
            'players': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '4'}),
            'buggy': forms.CheckboxInput(attrs={'class': 'form-check-input'})
            'booking_date'forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
            'booking_time'forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'})
        }

    def clean_booking_datetime(self):
        booking_datetime = self.cleaned_data.get('booking_date')
        if booking_datetime.tee_datetime < timezone.now():
            raise forms.ValidationError("Cannot select a date in the past.")
        return booking_datetime
