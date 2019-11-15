from django.db import models
from django.contrib.auth.models import AbstractUser
from contextlib import suppress

from django.db.models import Sum

from meetenjoy.enumeration import Enumeration

# TODO decompose

POSSIBLE_RATES = Enumeration([
    (1, "AWFUL"),
    (2, "BAD"),
    (3, "GOOD"),
    (4, "NICE"),
    (5, "AMAZING"),
])
USER_TYPE = Enumeration([
    (10, "VISITOR"),
    (20, "LECTOR"),
])


class User(AbstractUser):
    location = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=128, null=True, blank=True)

    def get_user_ref(self):
        return self.get_visitor() or self.get_lector()

    def get_lector(self):
        with suppress(Lector.DoesNotExist):
            return self.lector
        return None

    def get_visitor(self):
        with suppress(Visitor.DoesNotExist):
            return self.visitor
        return None

    def is_lector(self):
        return bool(self.get_lector())

    def is_visitor(self):
        return bool(self.get_visitor())


class Lector(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='lector')
    description = models.TextField(null=True, blank=True)

    @property
    def rate(self):
        return self.rate_summary / self.rate_count

    @property
    def rate_count(self):
        return self.rates.count()

    @property
    def rate_summary(self):
        return self.rates.all.aggregate(rate=Sum('rate')).get("rate", 1)


class Visitor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='visitor')

    @property
    def rated_lectors(self):
        return self.rates.values_list("lector", flat=True)


class Rate(models.Model):
    visitor = models.ForeignKey(Visitor, related_name="rates", on_delete=models.CASCADE)
    lector = models.ForeignKey(Lector, related_name="rates", on_delete=models.CASCADE)
    rate = models.SmallIntegerField(choices=POSSIBLE_RATES)
    comment = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = ("visitor", "lector")
