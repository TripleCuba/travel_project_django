from django.contrib import admin
from django.contrib.auth.models import User
from .models import Destination, Town, Hotel, Room, Order, Account, Profile

admin.site.register(Destination)
admin.site.register(Town)
admin.site.register(Hotel)
admin.site.register(Room)
admin.site.register(Order)
admin.site.register(Account)
admin.site.register(Profile)


