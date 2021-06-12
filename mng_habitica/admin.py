from django.contrib import admin
from mng_habitica.models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    pass
    # list_display = [
    #     'user_id', 'username', 'first_name', 'last_name',
    #     'language_code', 'deep_link',
    #     'created_at', 'updated_at', "is_blocked_bot",
    # ]
    # list_filter = ["is_blocked_bot", "is_moderator"]
    # search_fields = ('username', 'user_id')
    #
    # actions = ['broadcast']
    #
    # def invited_users(self, obj):
    #     return obj.invited_users().count()
