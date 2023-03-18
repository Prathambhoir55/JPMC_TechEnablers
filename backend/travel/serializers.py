from rest_framework import serializers
from .models import *
from .utils import *


class LocationSerializer(serializers.ModelSerializer):
    trip = serializers.CharField(read_only=True)
    city = serializers.CharField(read_only=True)
    state = serializers.CharField(read_only=True)
    country = serializers.CharField(read_only=True)

    class Meta:
        model = Location
        fields = ['trip', 'latitude', 'longitude', 'is_start', 'is_end', 'city', 'state', 'country']


class TripSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user = serializers.CharField(read_only=True)
    locations = LocationSerializer(source='trip', many=True)
    created_on = serializers.DateField(read_only=True)

    class Meta:
        model = Trip
        fields = ['id','user', 'locations', 'created_on', 'start_date', 'end_date','budget', 'adults', 'children']

    def create(self, validated_data, user):
        locations = validated_data.pop('trip')
        trip = Trip.objects.create(user=user, **validated_data)
        for location in locations:
            latitude = location['latitude']
            longitude = location['longitude']
            dict1 = geo_locate(str(latitude), str(longitude))
            loc = Location.objects.create(trip = trip, **location, **dict1)
        location_queryset = Location.objects.filter(trip=trip)
        path = optimal_path(location_queryset)
        validated_data['trip'] = locations
        validated_data['path'] = path
        itinerary = give_itinerary(validated_data, trip)
        return itinerary