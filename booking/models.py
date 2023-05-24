from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.


class TeeTime(models.Model):
    """Model for tee times"""
    objects = models.Manager()
    tee_datetime = models.DateTimeField(unique=True)
    max_players = models.IntegerField(default=4)
    available = models.BooleanField(default=True)

    def available_slots(self):
        booked_players = Booking.objects.filter(
            booking_datetime=self.tee_datetime).aggregate(
            total_players=models.Sum('players'))['total_players']
        if booked_players is None:
            booked_players = 0
        return self.max_players - booked_players

    def __str__(self):
        return f"{self.date} - {self.time}"


class Booking(models.Model):
    """Model for bookings"""
    objects = models.Manager()
    user_name = models.ForeignKey(User, on_delete=models.CASCADE)
    players = models.IntegerField(
        default=1,
        validators=[
            MaxValueValidator(4),
            MinValueValidator(1)
        ]
    )
    booking_datetime = models.ForeignKey(
        TeeTime, on_delete=models.CASCADE, to_field='tee_datetime', related_name='booking_datetime')
    buggy = models.BooleanField()

    # method only saves the booking if there is enough spaces on the tee time
    # and if the booking is saved it will check if there any remain spaces on
    # the tee time and update the availability

    def save(self, *args, **kwargs):
        tee_time = TeeTime.objects.get(
            tee_datetime=self.booking_datetime)
        available_slots = tee_time.available_slots()
        if available_slots < self.players:
            raise ValueError(
                f"You are trying to make a booking for {self.players} players, but this time only has space for {available_slots} players.")
        super().save(*args, **kwargs)
        tee_time.available = available_slots > 0
        tee_time.save()
