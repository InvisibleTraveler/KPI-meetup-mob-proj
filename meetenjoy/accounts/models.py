from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    description = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=128, null=True, blank=True)
    location = models.TextField(null=True, blank=True)
    rate_count = models.IntegerField(default=1)
    rate_summary = models.IntegerField(default=0)

    @property
    def rate(self):
        return self.rate_summary / self.rate_count
