from django import forms
from booking.models import Booking, TeeTime
from django.utils import timezone
from datetime import date, datetime, time


class EditBooking(forms.ModelForm):

    booking_datetime = forms.ModelChoiceField(
        queryset=TeeTime.objects.filter(tee_datetime__gte=timezone.now()),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Booking
        fields = ['booking_datetime', 'players', 'buggy']
        widgets = {
            'booking_datetime': forms.Select(attrs={'class': 'form-control'}),
            'players': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '4'}),
            'buggy': forms.CheckboxInput(attrs={'class': 'form-check-input'}),

        }

    # def __init__(self, *args, **kwargs):
    #     booking_instance = kwargs.get('instance', None)

    #     super(EditBooking, self).__init__(*args, **kwargs)

    #     # Set the default value of booking_datetime to the datetime of the booking being edited
    #     if booking_instance:
    #         self.fields['booking_datetime'].initial = booking_instance.booking_datetime
