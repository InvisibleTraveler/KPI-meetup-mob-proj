from django.shortcuts import render
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from .models import Meeting
from .serializers import MeetingSerializer


class MeetingView(RetrieveUpdateDestroyAPIView):
    serializer_class = MeetingSerializer
    queryset = Meeting.objects.all()

    class Meta:
        model = Meeting

