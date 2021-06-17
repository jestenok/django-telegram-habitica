import telegram
from telegram.ext import (
    Updater, Dispatcher, Filters,
    CommandHandler, MessageHandler,
    InlineQueryHandler, CallbackQueryHandler,
    ChosenInlineResultHandler,)
from manager.config import TG_API_KEY
from telegram_bot.handlers import admin, commands, files, location
from telegram_bot.handlers.commands import broadcast_command_with_message
from telegram_bot.handlers.handlers import comlete_task, broadcast_decision_handler
from telegram_bot.handlers.manage_data import CONFIRM_DECLINE_BROADCAST, COMPLETE_TASK
from telegram_bot.handlers.static_text import broadcast_command
from . import keyboard_utils, commands


def setup_dispatcher(dp):
    dp.add_handler(CommandHandler("start", keyboard_utils.keyboard))
    dp.add_handler(CommandHandler("task", commands.task))
    dp.add_handler(CommandHandler("tomorrow_tasks", commands.tomorrow_tasks))
    dp.add_handler(CommandHandler("nowdays_tasks", commands.nowdays_tasks))
    dp.add_handler(CommandHandler("admin", admin.admin))
    dp.add_handler(CommandHandler("stats", admin.stats))
    # dp.add_handler(CommandHandler("parse", commands.get_tasks))
    dp.add_handler(MessageHandler(Filters.text, commands.text_message))
    # dp.add_handler(CommandHandler("ask_location", location.ask_for_location))
    # dp.add_handler(MessageHandler(Filters.location, location.location_handler))
    # dp.add_handler(MessageHandler(Filters.animation, files.show_file_id,))
    dp.add_handler(CallbackQueryHandler(comlete_task, pattern=COMPLETE_TASK))
    # dp.add_handler(MessageHandler(Filters.regex(rf'^{broadcast_command} .*'), broadcast_command_with_message))
    # dp.add_handler(CallbackQueryHandler(broadcast_decision_handler, pattern=f"^{CONFIRM_DECLINE_BROADCAST}"))

    # EXAMPLES FOR HANDLERS
    # dp.add_handler(MessageHandler(Filters.text, <function_handler>))
    # dp.add_handler(MessageHandler(Filters.document, <function_handler>,))
    # dp.add_handler(CallbackQueryHandler(<function_handler>, pattern="^r\d+_\d+"))
    dp.add_handler(MessageHandler(Filters.photo, commands.photo))
    return dp


# @task(ignore_result=True)
def process_telegram_event(update_json):
    update = telegram.Update.de_json(update_json, bot)
    dispatcher.process_update(update)


bot = telegram.Bot(TG_API_KEY)
dispatcher = setup_dispatcher(Dispatcher(bot, None, workers=1, use_context=True))
