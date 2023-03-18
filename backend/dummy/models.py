from django.db import models
from accounts.models import *


class Hotel(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0)
    city = models.CharField(max_length=100)


class Attraction(models.Model):
    name = models.CharField(max_length=100)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0)
    city = models.CharField(max_length=100)


class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0)
    city = models.CharField(max_length=100)