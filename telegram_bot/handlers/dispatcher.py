import telegram
from telegram.ext import (
    Updater, Dispatcher, Filters,
    CommandHandler, MessageHandler,
    InlineQueryHandler, CallbackQueryHandler,
    ChosenInlineResultHandler,)
from manager.config import TG_API_KEY
from telegram_bot.handlers import admin, commands, files, location
from telegram_bot.handlers.commands import broadcast_command_with_message
from telegram_bot.handlers.handlers import secret_level, broadcast_decision_handler
from telegram_bot.handlers.manage_data import SECRET_LEVEL_BUTTON, CONFIRM_DECLINE_BROADCAST
from telegram_bot.handlers.static_text import broadcast_command
from . import keyboard_utils, commands


def setup_dispatcher(dp):
    dp.add_handler(CommandHandler("start", keyboard_utils.keyboard))
    dp.add_handler(CommandHandler("task", commands.task))
    dp.add_handler(CommandHandler("admin", admin.admin))
    dp.add_handler(CommandHandler("stats", admin.stats))
    dp.add_handler(MessageHandler(Filters.text, commands.text_message))
    dp.add_handler(CommandHandler("ask_location", location.ask_for_location))
    dp.add_handler(MessageHandler(Filters.location, location.location_handler))
    dp.add_handler(MessageHandler(Filters.animation, files.show_file_id,))
    dp.add_handler(CallbackQueryHandler(secret_level, pattern=f"^{SECRET_LEVEL_BUTTON}"))
    dp.add_handler(MessageHandler(Filters.regex(rf'^{broadcast_command} .*'), broadcast_command_with_message))
    dp.add_handler(CallbackQueryHandler(broadcast_decision_handler, pattern=f"^{CONFIRM_DECLINE_BROADCAST}"))

    # EXAMPLES FOR HANDLERS
    # dp.add_handler(MessageHandler(Filters.text, <function_handler>))
    # dp.add_handler(MessageHandler(Filters.document, <function_handler>,))
    # dp.add_handler(CallbackQueryHandler(<function_handler>, pattern="^r\d+_\d+"))
    # dp.add_handler(MessageHandler(Filters.chat(chat_id=int(TELEGRAM_FILESTORAGE_ID)),
    #     & Filters.forwarded & (Filters.photo | Filters.video | Filters.animation),
    #     <function_handler>,))
    return dp


# @task(ignore_result=True)
def process_telegram_event(update_json):
    update = telegram.Update.de_json(update_json, bot)
    dispatcher.process_update(update)


def habitica_task_compleeted(task):
    comment = ''
    if task.notes != '':
        comment = 'Комментарий: {notes}'.format(notes=task.notes)
    text = 'Задача № {task_number} ({text}) выполнена! {comment}'.format(task_number=task.task_number,
                                                                         text=task.text,
                                                                         comment=comment)
    bot.send_message(chat_id=task.user_telegram_id, text=text)


bot = telegram.Bot(TG_API_KEY)
dispatcher = setup_dispatcher(Dispatcher(bot, None, workers=1, use_context=True))
TELEGRAM_BOT_USERNAME = bot.get_me()["username"]

