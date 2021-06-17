from django.contrib import admin
from manager1c.models import Message


@admin.register(Message)
class TaskAdmin(admin.ModelAdmin):
    pass