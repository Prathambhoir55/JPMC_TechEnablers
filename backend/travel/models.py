from django.db import models
from accounts.models import User
    

class Trip(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateField(auto_now_add=True)
    budget = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    start_date = models.DateField()
    end_date = models.DateField()
    adults = models.IntegerField(default=1)
    children = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id)

class Location(models.Model):

    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='trip')
    latitude = models.DecimalField(max_digits=8, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=8, decimal_places=6, blank=True, null=True)
    is_start = models.BooleanField(default=False)
    is_end = models.BooleanField(default=False)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)