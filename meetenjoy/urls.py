from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
from meetings.urls import urlpatterns as meeting_urlpatterns
from accounts.urls import urlpatterns as accounts_urlpatterns

API_V1 = 'api/v1/'
urlpatterns = [
    path('admin/', admin.site.urls),
    path(API_V1, include("rest_auth.urls")),

    path(f"{API_V1}meeting/", include(meeting_urlpatterns)),
    path(f"{API_V1}account/", include(accounts_urlpatterns)),

] + staticfiles_urlpatterns()
