from django.contrib import admin
from .models import *


class TripAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_on','budget', 'adults', 'children']
    list_filter = ['id', 'user', 'created_on','budget', 'adults', 'children']


class LocationAdmin(admin.ModelAdmin):
    list_display = ['trip', 'latitude', 'longitude', 'is_start', 'is_end', 'city', 'state', 'country']
    list_filter = ['trip', 'latitude', 'longitude', 'is_start', 'is_end', 'city', 'state', 'country']


admin.site.register(Trip, TripAdmin)
admin.site.register(Location, LocationAdmin)
