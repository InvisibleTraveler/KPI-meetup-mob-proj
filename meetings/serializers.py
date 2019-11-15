from rest_framework import serializers

from accounts.serializers import VisitorSerializer, LectorSerializer
from .models import Meeting, Tag


class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = (
            "id",
            "title",
            "description",
            "created_at",
            "published_at",
            "start_at",
            "duration",
            "status",
            "location",
            "is_main",
            "from_site",
            "from_url",
            "creator",
            "participants",
        )
        read_only_fields = ("created_at", "participants", "is_main", "from_site", "from_url")


class ReadOnlyMeetingSerializer(serializers.ModelSerializer):
    creator = LectorSerializer(read_only=True)
    participants = VisitorSerializer(many=True, read_only=True)

    class Meta:
        model = Meeting
        fields = (
            "id",
            "title",
            "description",
            "created_at",
            "published_at",
            "start_at",
            "duration",
            "status",
            "location",
            "is_main",
            "from_site",
            "from_url",
            "creator",
            "participants",
        )
        read_only_fields = fields

    def create(self, validated_data):
        assert False

    def update(self, instance, validated_data):
        assert False


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"
