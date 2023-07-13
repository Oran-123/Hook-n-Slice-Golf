from django import forms
from booking.models import Booking, TeeTime


class EditBooking(forms.ModelForm):
    booking_datetime = forms.ModelChoiceField(queryset=TeeTime.objects.all(
    ), widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Booking
        fields = ['booking_datetime', 'players', 'buggy']
        widgets = {
            'players': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '4'}),
            'buggy': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }
