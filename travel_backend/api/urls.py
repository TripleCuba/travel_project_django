from django.urls import path
from travel_backend.api.views import get_destination_list, get_destination, get_town_list, get_town, get_hotel_list, \
    get_hotel, get_room_list, get_room, reserve_room, get_user_reservations, cancel_reservation
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('destination_list/', get_destination_list),
    path('destination/<id>', get_destination),
    path('town_list/<id>', get_town_list),
    path('town/<id>', get_town),
    path('hotel_list/<id>', get_hotel_list),
    path('hotel/<id>', get_hotel),
    path('room_list/<id>', get_room_list),
    path('room/<id>', get_room),
    path('reserveRoom/<id>', reserve_room),
    path('cancelReservation/<id>', cancel_reservation),
    path('reservations/', get_user_reservations)

]
