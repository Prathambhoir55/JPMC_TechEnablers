from django.urls import path, include
from .views import *

urlpatterns = [
    path('trip-post/', TripAPI.as_view(), name = 'trip-post'),
    path('trip-list/', TripListAPI.as_view(), name = 'trip-list'),
]
