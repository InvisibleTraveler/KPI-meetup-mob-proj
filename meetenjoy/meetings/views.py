from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView, CreateAPIView, RetrieveAPIView, \
    GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from meetenjoy.core import IsLector
from .models import Meeting, MeetingStatus
from .serializers import MeetingSerializer, ReadOnlyMeetingSerializer


class MeetingCreateView(CreateAPIView):
    serializer_class = MeetingSerializer
    permission_classes = [IsAuthenticated, IsLector]

    class Meta:
        model = Meeting

    def create(self, request, *args, **kwargs):
        lector = request.user.lector
        data = {
            "title": request.data.get("title"),
            "description": request.data.get("description"),
            "start_at": request.data.get("start_at") or None,
            "duration": request.data.get("duration") or None,
            "status": request.data.get("status"),
            "location": request.data.get("location"),
            "creator": lector.id,
        }
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=data)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UpdateDestroyMeetingView(RetrieveUpdateDestroyAPIView):
    serializer_class = MeetingSerializer
    permission_classes = [IsAuthenticated, IsLector]

    def get_queryset(self):
        return self.request.user.lector.created_meetings

    class Meta:
        model = Meeting


class RetrieveMeetingView(RetrieveAPIView):
    serializer_class = ReadOnlyMeetingSerializer
    queryset = Meeting.objects.all()

    class Meta:
        model = Meeting


class MeetingListView(ListAPIView):
    serializer_class = ReadOnlyMeetingSerializer
    queryset = Meeting.objects.published()

    class Meta:
        model = Meeting


class VisitorSubscribeToMeeting(GenericAPIView):
    ...
