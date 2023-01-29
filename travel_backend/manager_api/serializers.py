from rest_framework import serializers
from travel_backend.models import Destination, Town, Hotel, Room


class AddDestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = ['destination', 'description', 'image']


class EditDestinationSerializer(serializers.ModelSerializer):
    destination = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    image = serializers.ImageField(required=False)

    class Meta:
        model = Destination
        fields = ['destination', 'description', 'image']


class AddTownSerializer(serializers.ModelSerializer):
    class Meta:
        model = Town
        fields = ['title', 'destination', 'description', 'image']


class AddHotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = ['title', 'town', 'image']


class AddRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['title', 'capacity', 'price_per_guest', 'room_number', 'hotel']
