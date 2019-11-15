from accounts.views import (
    RegistrationAPIView, RetrieveUpdateUserAPIView, RetrieveUpdateLectorAPIView, RetrieveUpdateVisitorAPIView,
    CreateRateLectorView, UpdateRateLectorView, LectorListAPIView)
from django.urls import path

urlpatterns = [
    path('registration/', RegistrationAPIView.as_view()),
    path('user/', RetrieveUpdateUserAPIView.as_view()),
    path('lector/', RetrieveUpdateLectorAPIView.as_view()),
    path('lectors/', LectorListAPIView.as_view()),
    path('visitor/', RetrieveUpdateVisitorAPIView.as_view()),
    path('rate/', CreateRateLectorView.as_view()),
    path('rate/<int:pk>/', UpdateRateLectorView.as_view()),
]
