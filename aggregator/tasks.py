from meetenjoy import celery_app
from django.db import transaction

from aggregator.loader.dou import DOUApi, DOULoader
from aggregator.loader.meetup import MeetupApi, MeetupLoader


def load(_api, _loader):
    api = _api()
    loader = _loader(api)
    with transaction.atomic():
        return loader.load_meetings()


@celery_app.task
def load_dou_meetings():
    load(DOUApi, DOULoader)


@celery_app.task
def load_meetup_meetings():
    load(MeetupApi, MeetupLoader)
