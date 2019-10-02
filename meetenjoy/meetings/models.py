from enum import Enum

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class MeetingStatus(Enum):
    DRAFT = 0
    PUBLISHED = 1
    CANCELED = 2
    DELETED = 3
    FINISHED = 4

    @staticmethod
    def choices():
        return (
            (MeetingStatus.DRAFT, 'Draft'),
            (MeetingStatus.PUBLISHED, 'Published'),
            (MeetingStatus.CANCELED, 'Canceled'),
            (MeetingStatus.DELETED, 'Deleted'),
            (MeetingStatus.FINISHED, 'Finished'),
        )


class Meeting(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    start_at = models.DateTimeField(null=True, blank=True)
    duration = models.TimeField(null=True, blank=True)
    status = models.PositiveSmallIntegerField(choices=(MeetingStatus.choices()), default=MeetingStatus.DRAFT)
    location = models.TextField()

    is_main = models.BooleanField(default=True)
    from_site = models.CharField(max_length=128, blank=True, default=True)
    from_url = models.CharField(max_length=256, null=True, blank=True)

    creator = models.ForeignKey(User, related_name="created_meetings",
                                on_delete=models.SET_NULL, null=True, blank=True)
    participants = models.ManyToManyField(User, related_name="following_meetings")


class Tag(models.Model):
    name = models.CharField(max_length=64)
    meetings = models.ManyToManyField("meetings.Meeting", related_name="tags")
    users = models.ManyToManyField(User, related_name="tags")
