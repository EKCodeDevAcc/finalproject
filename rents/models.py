from django.db import models
from django.conf import settings

# Create your models here.
class Location(models.Model):
    location_name = models.CharField(max_length=64)
    location_address = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.location_name} {self.location_address}"


class Car(models.Model):
    car_brand = models.CharField(max_length=64)
    car_name = models.CharField(max_length=64)
    car_type = models.CharField(max_length=64)
    car_price = models.FloatField()
    car_size = models.IntegerField()
    car_detail = models.CharField(max_length=64)
    car_status = models.CharField(max_length=64)
    car_location = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.car_brand} {self.car_name} {self.car_type} {self.car_price} {self.car_size} {self.car_detail}"


class Reservation(models.Model):
    reservation_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reservation_car = models.ForeignKey(Car, on_delete=models.CASCADE)
    reservation_start_date = models.DateTimeField()
    reservation_end_date = models.DateTimeField()
    reservation_pick_up = models.CharField(max_length=64)
    reservation_drop_off = models.CharField(max_length=64)
    reservation_protection = models.CharField(max_length=64)
    reservation_total_price = models.FloatField()
    reservation_status = models.CharField(max_length=64)
    reservation_request = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.reservation_user} {self.reservation_car} {self.reservation_protection} {self.reservation_total_price} {self.reservation_status} {self.reservation_status}"


class ReservedDate(models.Model):
    reserved_date_car = models.ForeignKey(Car, on_delete=models.CASCADE)
    reserved_date_reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    reserved_date_start_date = models.DateTimeField()
    reserved_date_end_date = models.DateTimeField()

    def __str__(self):
        return f"{self.reserved_date_car} {self.reserved_date_start_date} {self.reserved_date_end_date}"


class Request(models.Model):
    request_reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    request_reserved_date = models.ForeignKey(ReservedDate, on_delete=models.CASCADE)
    request_start_date = models.DateTimeField(blank=True, null=True)
    request_end_date = models.DateTimeField(blank=True, null=True)
    request_pick_up = models.CharField(max_length=64)
    request_drop_off = models.CharField(max_length=64)
    request_status = models.CharField(max_length=64)
    request_approval = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.request_reservation} {self.request_start_date} {self.request_end_date} {self.request_pick_up} {self.request_drop_off} {self.request_status} {self.request_approval}"