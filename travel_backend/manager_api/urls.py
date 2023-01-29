from django.urls import path
from travel_backend.manager_api.views import add_destination, add_town, add_hotel, add_room,delete_destination, edit_destination

urlpatterns = [
    path('add_destination/', add_destination),
    path('add_town/', add_town),
    path('add_hotel/', add_hotel),
    path('add_room/', add_room),
    path('delete_destination/<id>', delete_destination),
    path('update_destination/<id>', edit_destination),
]