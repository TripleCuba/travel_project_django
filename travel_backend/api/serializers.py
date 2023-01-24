from rest_framework import serializers
from travel_backend.models import Destination, Town, Hotel, Room, Order


class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = '__all__'


class TownSerializer(serializers.ModelSerializer):
    destination = DestinationSerializer(many=False)

    class Meta:
        model = Town
        fields = '__all__'


class HotelSerializer(serializers.ModelSerializer):
    town = TownSerializer(many=False)

    class Meta:
        model = Hotel
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):
    hotel = HotelSerializer(many=False)

    class Meta:
        model = Room
        fields = '__all__'


class RoomUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['is_available']


class OrderSerializer(serializers.ModelSerializer):
    room = RoomSerializer(many=False)

    class Meta:
        model = Order
        fields = '__all__'


class CrateOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'
