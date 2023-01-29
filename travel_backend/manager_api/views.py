from rest_framework.response import Response
from travel_backend.models import Destination, Town, Hotel, Room
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from travel_backend.manager_api.serializers import AddDestinationSerializer, AddTownSerializer, AddHotelSerializer, \
    AddRoomSerializer, EditDestinationSerializer


@api_view(['POST'])
@permission_classes((IsAuthenticated, IsAdminUser))
def add_destination(request):
    full_obj = request.data
    print(full_obj)
    serializer = AddDestinationSerializer(data=full_obj)
    if serializer.is_valid():
        destination = serializer.save()
        data = {'message': 'success',
                }
    else:
        data = {'message': 'error'}
    return Response(data)


@api_view(['POST'])
@permission_classes((IsAuthenticated, IsAdminUser))
def add_town(request):
    full_obj = request.data
    print(full_obj)
    serializer = AddTownSerializer(data=full_obj)
    if serializer.is_valid():
        town = serializer.save()
        data = {'message': 'success'}
    else:
        data = {'message': 'error'}
    return Response(data)


@api_view(['POST'])
@permission_classes((IsAuthenticated, IsAdminUser))
def add_hotel(request):
    full_obj = request.data
    print(full_obj)
    serializer = AddHotelSerializer(data=full_obj)
    if serializer.is_valid():
        hotel = serializer.save()
        print(hotel)
        data = {'message': 'success'}
    else:
        data = {'message': 'error'}
    return Response(data)


@api_view(['POST'])
@permission_classes((IsAuthenticated, IsAdminUser))
def add_room(request):
    full_obj = request.data
    print(full_obj)
    serializer = AddRoomSerializer(data=full_obj)
    if serializer.error_messages:
        for i in serializer.error_messages:
            print(i)
    if serializer.is_valid():
        room = serializer.save()
        print(room)
        data = {'message': 'success'}
    else:
        data = {'message': 'error'}
    return Response(data)


@api_view(['DELETE'])
@permission_classes((IsAuthenticated, IsAdminUser))
def delete_destination(request, id):
    destination = Destination.objects.filter(id=id).first()
    if destination:
        destination.delete()
        data = {'message': 'delete completed',
                'is_success': True}
    else:
        data = {'message': 'There seems to be a problem',
                'is_success': False}
    return Response(data)


@api_view(['PATCH'])
@permission_classes((IsAuthenticated, IsAdminUser))
def edit_destination(request, id):
    print(request.data)
    destination = Destination.objects.filter(id=id).first()
    serializer = EditDestinationSerializer(instance=destination, data=request.data)
    if serializer.is_valid():
        serializer.save()
        data = {'message': 'success',
                'is_success': True}
    else:
        data = {'message': 'error',
                'is_success': False}
    return Response(data)
