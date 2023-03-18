from django.contrib import admin
from .models import *


class HotelAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'rating', 'city']
    list_filter = ['name', 'price', 'rating', 'city']


class AttractionAdmin(admin.ModelAdmin):
    list_display = ['name', 'rating', 'city']
    list_filter = ['name', 'rating', 'city']


class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'rating', 'city']
    list_filter = ['name', 'price', 'rating', 'city']


admin.site.register(Hotel, HotelAdmin)
admin.site.register(Attraction, AttractionAdmin)
admin.site.register(Restaurant, RestaurantAdmin)