from django import forms
from booking.models import Booking, TeeTime
from django.utils import timezone
from datetime import date, datetime, time


class EditBooking(forms.ModelForm):

    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

        self.fields['booking_datetime'].queryset = TeeTime.objects.filter(
            tee_datetime__gte=timezone.now())

    class Meta:
        model = Booking
        fields = ['booking_datetime', 'players', 'buggy']
        widgets = {
            'booking_datetime': forms.Select(attrs={'class': 'form-control'}),
            'players': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '4'}),
            'buggy': forms.CheckboxInput(attrs={'class': 'form-check-input'}),

        }

    def clean(self):
        cleaned_data = super().clean()
        booking_datetime = cleaned_data.get('booking_datetime')
        players = cleaned_data.get('players')
        booking_date = booking_datetime.tee_datetime.date()
        user_name = Booking.user_name

        existing_booking = Booking.objects.filter(
            user_name=self.user,
            booking_datetime__tee_datetime__date=booking_datetime.tee_datetime.date()
        ).first()

        if existing_booking:
            self.add_error(
                'booking_datetime', f"You have already booked a tee time on {booking_datetime.tee_datetime.date()}. You are only permitted to make one booking per day.")
