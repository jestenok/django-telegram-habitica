import random
import telegram
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.shortcuts import render

from manager.settings import DEBUG

from telegram_bot.models import Location, Arcgis
from telegram_bot.models import User, UserActionLog
from telegram_bot.forms import BroadcastForm
from telegram_bot.handlers import utils



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



@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'created_at']


@admin.register(Arcgis)
class ArcgisAdmin(admin.ModelAdmin):
    list_display = ['location', 'city', 'country_code']


@admin.register(UserActionLog)
class UserActionLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'created_at']