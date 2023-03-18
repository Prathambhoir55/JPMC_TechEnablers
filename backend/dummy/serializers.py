from rest_framework import serializers
from .models import *
from .utils import *

class HotelSerializer(serializers.Serializer):
    name = serializers.CharField(read_only = True)
    price = serializers.DecimalField(max_digits=12, decimal_places=2, read_only = True)
    rating = serializers.DecimalField(max_digits=12, decimal_places=2, read_only = True)

    class Meta:
        model = Hotel
        fields = ['name', 'price', 'rating', 'city']

    def create(self, validated_data):
        city = validated_data['city']
        geoId = give_geoid(city)
        pass
