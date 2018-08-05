from django.contrib import admin

from .models import Location, Car, Reservation, ReservedDate, Request

# Register your models here.
admin.site.register(Location)
admin.site.register(Car)
admin.site.register(Reservation)
admin.site.register(ReservedDate)
admin.site.register(Request)