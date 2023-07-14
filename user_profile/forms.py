from django import forms
from booking.models import Booking, TeeTime
from django.utils import timezone



class EditBooking(forms.ModelForm):
    booking_datetime = forms.ModelChoiceField(
        queryset=TeeTime.objects.filter(tee_datetime__gte=timezone.now()),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Booking
        fields = ['booking_datetime', 'players', 'buggy']
        widgets = {
            'players': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '4'}),
            'buggy': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }

    def clean_booking_datetime(self):
        booking_datetime = self.cleaned_data.get('booking_datetime')
        if booking_datetime < timezone.now():
            raise forms.ValidationError("Cannot select a date in the past.")
        return booking_datetime
