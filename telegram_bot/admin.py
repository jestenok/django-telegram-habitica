from django.contrib import admin
from telegram_bot.models import User, Logs, UserMessages, Message, Task


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'user_id', 'username', 'first_name', 'last_name', 
        'language_code', 'deep_link',
        'created_at', 'updated_at', "is_blocked_bot",
    ]
    list_filter = ["is_blocked_bot", "is_moderator"]
    search_fields = ('username', 'user_id')

    actions = ['broadcast']

    def invited_users(self, obj):
        return obj.invited_users().count()



@admin.register(Logs)
class LocationAdmin(admin.ModelAdmin):
     list_display = ['date', 'log_type', 'user', 'text']


@admin.register(UserMessages)
class LocationAdmin(admin.ModelAdmin):
     list_display = ['date', 'user', 'text']


@admin.register(Message)
class TaskAdmin(admin.ModelAdmin):
    pass


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    pass