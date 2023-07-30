"""
Booking App - Views
---------------------
Views for booking app

"""

# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from django.contrib import admin
from rangefilter.filters import (
    DateRangeFilterBuilder,
    DateTimeRangeFilterBuilder,
    NumericRangeFilterBuilder,
)
from .models import Booking, TeeTime
from django.contrib.auth.models import User
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    """
    Admin configuration for Booking model.
    """
    list_display = ('user_name', 'players', 'booking_datetime', 'buggy')
    list_filter = (
        ("booking_datetime", DateRangeFilterBuilder()),)
    search_fields = ['user_name__username']


@admin.register(TeeTime)
class TeeTimeAdmin(admin.ModelAdmin):
    """
    Admin configuration for TeeTime model.
    """
    list_display = ('tee_datetime', 'available', 'booked_players')
    list_filter = ('available', ("tee_datetime", DateRangeFilterBuilder()))

    def booked_players(self, obj):
        return obj.available_slots()

    booked_players.short_description = "Available Spaces"
