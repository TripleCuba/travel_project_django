from rest_framework.response import Response
from travel_backend.models import Destination, Town, Hotel, Room, Order
from travel_backend.api.serializers import DestinationSerializer, TownSerializer, HotelSerializer, RoomSerializer, \
    RoomUpdateSerializer, OrderSerializer, CrateOrderSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


@api_view()
def get_destination_list(request):
    destinations = Destination.objects.all()
    serializer = DestinationSerializer(destinations, many=True)
    return Response(serializer.data)


@api_view()
def get_destination(request, id):
    destination = Destination.objects.filter(id=id).first()
    serializer = DestinationSerializer(destination, many=False)
    return Response(serializer.data)


@api_view()
def get_all_towns(request):
    towns = Town.objects.all()
    serializer = TownSerializer(towns, many=True)
    return Response(serializer.data)

@api_view()
def get_town_list(request, id):
    towns = Town.objects.filter(destination=id).all()
    serializer = TownSerializer(towns, many=True)
    return Response(serializer.data)


@api_view()
def get_town(request, id):
    town = Town.objects.filter(id=id).first()
    print(town)
    if town:
        serializer = TownSerializer(town, many=False)
        data = serializer.data
    else:
        data = {'message': 'town does not exist'}
    return Response(data)


@api_view()
def get_hotel_list(request, id):
    hotels = Hotel.objects.filter(town=id).all()
    serializer = HotelSerializer(hotels, many=True)
    return Response(serializer.data)

@api_view()
def get_all_hotels(request):
    hotels = Hotel.objects.all()
    serializer = HotelSerializer(hotels, many=True)
    return Response(serializer.data)


@api_view()
def get_hotel(request, id):
    hotel = Hotel.objects.filter(id=id).first()
    if hotel:
        serializer = HotelSerializer(hotel, many=False)
        data = serializer.data
    else:
        data = {'message': 'hotel does not exist'}
    return Response(data)


@api_view()
def get_room_list(request, id):
    rooms = Room.objects.filter(hotel__id=id, is_available=True).all()
    data = []
    if rooms:
        serializer = RoomSerializer(rooms, many=True)
        data = serializer.data
    else:
        data = []
    return Response(data)


@api_view()
def get_room(request, id):
    room = Room.objects.filter(id=id).first()
    if room:
        serializer = RoomSerializer(room, many=False)
        data = serializer.data
    else:
        data = {'message': 'room does not exist'}
    return Response(data)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def reserve_room(request, id):
    user = request.user
    guests = request.data['guests']
    total_price = request.data['totalPrice']

    room = Room.objects.filter(id=id).first()
    if room and room.is_available:
        room_serializer = RoomUpdateSerializer(instance=room, data={'is_available': False})
        room.is_available = False
        order_serializer = CrateOrderSerializer(data={
            'user': user.id,
            'room': room.id,
            'guests': guests,
            'total_price': total_price
        })
        if room_serializer.is_valid() and order_serializer.is_valid():
            room_serializer.save()
            order_serializer.save()

            data = {
                'message': 'Room reserved successfully',
                'is_success': True
            }
        else:
            data = {
                'message': 'something is wrong',
                'is_success': False
            }
    else:
        data = {'message': 'room is not available',
                'is_success': False}

    return Response(data)


@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
def cancel_reservation(request, id):
    order = Order.objects.filter(id=id).first()
    room = Room.objects.filter(id=order.room.id).first()
    if order.user.id == request.user.id:
        room_serializer = RoomUpdateSerializer(instance=room, data={'is_available': True})
        if room_serializer.is_valid():
            room_serializer.save()
            order.delete()
            data = {'message': 'Order canceled successfully',
                    'is_success': True},
        else:
            data = {'message': 'Something is wrong',
                    'is_success': False, }
    else:
        data = {'message': 'user is unauthorised to do this!',
                'is_success': False, }

    return Response(data[0])


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_user_reservations(request):
    user = request.user.id
    orders = Order.objects.filter(user=user).all()
    if orders:
        serializer = OrderSerializer(orders, many=True)
        data = serializer.data
    else:
        message = {'message': 'This account does not have any reservations'}
        data = message
    return Response(data)
