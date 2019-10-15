from django.contrib import admin
from django.urls import path, include
from meetings.urls import urlpatterns as meeting_urlpatterns

API_V1 = 'api/v1/'
urlpatterns = [
    path('admin/', admin.site.urls),
    path(API_V1, include(meeting_urlpatterns)),
]
