from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime


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

    # class method creates tee times for the next 7 days when called by signal
    @classmethod
    def create_tee_times(cls):
        start_date = datetime.date.today()
        # Generate tee times for the next 7 days
        end_date = start_date + datetime.timedelta(days=7)

        start_time = datetime.time(9)  # Start generating tee times from 9am
        end_time = datetime.time(17)  # Generate tee times until 5pm

        current_date = start_date

        while current_date <= end_date:
            current_datetime = datetime.datetime.combine(
                current_date, start_time)

            while current_datetime.time() <= end_time:
                tee_time, created = cls.objects.get_or_create(
                    tee_datetime=current_datetime)
                if created:
                    tee_time.save()

                current_datetime += datetime.timedelta(hours=1)

            current_date += datetime.timedelta(days=1)

    def __str__(self):
        return f"{self.tee_datetime}"


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
            tee_datetime=self.booking_datetime.tee_datetime)
        available_slots = tee_time.available_slots()

        players = int(self.players)

        if available_slots < players:
            raise ValueError(
                f"You are trying to make a booking for {self.players} players, but this time only has space for {available_slots} players.")
        super().save(*args, **kwargs)
        tee_time.available = available_slots > 0
        tee_time.save()


# signal creates teetimes everytime a booking is made
@receiver(post_save, sender=Booking)
def generate_tee_times(sender, instance, created, **kwargs):
    if created:
        TeeTime.create_tee_times()
