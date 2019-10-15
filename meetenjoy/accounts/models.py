from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    location = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=128, null=True, blank=True)

    @property
    def rate(self):
        return self.rate_summary / self.rate_count


class Lector(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='lector')
    description = models.TextField(null=True, blank=True)
    rate_count = models.IntegerField(default=1)
    rate_summary = models.IntegerField(default=0)


class Visitor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='visitor')
