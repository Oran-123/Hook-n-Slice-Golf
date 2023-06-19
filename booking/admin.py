from django.contrib import admin
from rangefilter.filters import DateRangeFilterBuilder, DateTimeRangeFilterBuilder, NumericRangeFilterBuilder
from .models import Booking, TeeTime


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'players', 'booking_datetime', 'buggy')
    list_filter = (
        ("booking_datetime", DateRangeFilterBuilder()),)


@admin.register(TeeTime)
class TeeTimeAdmin(admin.ModelAdmin):
    list_display = ('tee_datetime', 'available', 'booked_players')
    list_filter = ('available',)
    search_fields = ("tee_datetime", DateRangeFilterBuilder())

    def booked_players(self, obj):
        return obj.available_slots()

    booked_players.short_description = "Available Spaces"
