from django.urls import path
from .views import registration_view, get_user_view, update_profile, get_profile_view, update_profile_image
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('register/', registration_view),
    path('login/', obtain_auth_token),
    path('get_user/', get_user_view),
    path('get_profile/', get_profile_view),
    path('update_profile/', update_profile),
    path('update_profile_img/', update_profile_image),

]