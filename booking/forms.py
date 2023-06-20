from django import forms
from django.forms.widgets import CheckboxSelectMultiple
from .models import Booking, TeeTime


class TeeTimeForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(
        attrs={'class': 'form-control', 'type': 'date'}))
    start_time = forms.TimeField(widget=forms.TimeInput(
        attrs={'class': 'form-control', 'type': 'time'}))
    end_time = forms.TimeField(widget=forms.TimeInput(
        attrs={'class': 'form-control', 'type': 'time'}))
    players = forms.IntegerField(widget=forms.NumberInput(
        attrs={'class': 'form-control', 'min': '1', 'max': '4'}))

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_time and end_time and start_time >= end_time:
            self.add_error(
                'end_time', 'End time must be later than start time.')

    def get_available_tee_times(self):
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