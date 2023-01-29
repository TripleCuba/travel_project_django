from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', include('travel_backend.api.urls')),
                  path('accounts/', include('travel_backend.user_api.urls')),
                  path('manager/', include('travel_backend.manager_api.urls')),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
