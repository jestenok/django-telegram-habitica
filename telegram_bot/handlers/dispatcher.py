import telegram
from telegram.ext import (
    Updater, Dispatcher, Filters,
    CommandHandler, MessageHandler,
    InlineQueryHandler, CallbackQueryHandler,
    ChosenInlineResultHandler,)
from manager.config import TG_API_KEY
from . import admin
from .commands import broadcast_command_with_message
from .handlers import comlete_task, broadcast_decision_handler, anime_action
from .manage_data import CONFIRM_DECLINE_BROADCAST, COMPLETE_TASK, ANIME, PLANNED, VIEWED
from .static_text import broadcast_command
from . import keyboard_utils, commands


def setup_dispatcher(dp):
    dp.add_handler(CommandHandler("start", keyboard_utils.keyboard))
    dp.add_handler(CommandHandler("task", commands.task))
    dp.add_handler(CommandHandler("yesterday_tasks", commands.yesterday_tasks))
    dp.add_handler(CommandHandler("nowdays_tasks", commands.nowdays_tasks))
    dp.add_handler(CommandHandler("admin", admin.admin))
    dp.add_handler(CommandHandler("stats", admin.stats))
    dp.add_handler(CommandHandler("announcement", commands.announcement))
    dp.add_handler(CommandHandler("anime", commands.anime))
    dp.add_handler(CommandHandler("mylist", commands.mylist))
    dp.add_handler(MessageHandler(Filters.text, commands.text_message))
    dp.add_handler(MessageHandler(Filters.photo, commands.text_message))
    dp.add_handler(CallbackQueryHandler(comlete_task, pattern=COMPLETE_TASK))
    dp.add_handler(CallbackQueryHandler(anime_action, pattern=PLANNED))
    dp.add_handler(CallbackQueryHandler(anime_action, pattern=VIEWED))
    return dp


# @task(ignore_result=True)
def process_telegram_event(update_json):
    update = telegram.Update.de_json(update_json, bot)
    dispatcher.process_update(update)


bot = telegram.Bot(TG_API_KEY)
dispatcher = setup_dispatcher(Dispatcher(bot, None, workers=1, use_context=True))
