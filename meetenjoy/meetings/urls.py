from django.urls import path, include
from rest_framework.routers import DefaultRouter
from meetings import views
#
# router = DefaultRouter()
# router.register(r'meeting', views.MeetingView)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('meeting/<int:pk>', views.MeetingView.as_view()),
    # path('meeting/', include(router.urls)),
]