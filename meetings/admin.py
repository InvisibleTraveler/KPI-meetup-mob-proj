from django.contrib import admin
from .models import Meeting


@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at", "start_at")
    list_filter = ("title", "created_at")
    search_fields = ("title",)
