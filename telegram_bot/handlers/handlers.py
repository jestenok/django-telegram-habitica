import datetime
import telegram

from mng_habitica.handlers.commands import task_create, task_update
from mng_habitica.models import Task
from telegram_bot.handlers.manage_data import CONFIRM_DECLINE_BROADCAST, CONFIRM_BROADCAST, COMPLETE_TASK, PLANNED, VIEWED
from telegram_bot.handlers.static_text import unlock_secret_room, message_is_sent, task_text
from telegram_bot.handlers.utils import handler_logging
from telegram_bot.models import User
from telegram_bot.utils import extract_user_data_from_update
from django.utils import timezone


@handler_logging()
def comlete_task(update, context):
    user_id = extract_user_data_from_update(update)['user_id']
    task_number = update.callback_query.data[len(COMPLETE_TASK):]
    task = Task.task_get(task_number)
    # task.completed = True
    # task.save()
    text = task_text(task)
    task_update(task)

    context.bot.edit_message_text(
        text=text,
        chat_id=user_id,
        message_id=update.callback_query.message.message_id,
        parse_mode=telegram.ParseMode.HTML
    )


@handler_logging()
def anime_action(update, context):
    user_id = extract_user_data_from_update(update)['user_id']
    text = update.callback_query.data
    if text.find(PLANNED) != -1 :
        pass
        # context.bot.edit_message_text(
        #     text="Запланировано",
        #     chat_id=user_id,
        #     message_id=update.callback_query.message.message_id,
        #     parse_mode=telegram.ParseMode.HTML
        # )
    else:
        pass
        # context.bot.edit_message_text(
        #     text="Просмотрено",
        #     chat_id=user_id,
        #     message_id=update.callback_query.message.message_id,
        #     parse_mode=telegram.ParseMode.HTML
        # )


def broadcast_decision_handler(update, context): #callback_data: CONFIRM_DECLINE_BROADCAST variable from manage_data.py
    """ Entered /broadcast <some_text>.
        Shows text in Markdown style with two buttons:
        Confirm and Decline
    """
    broadcast_decision = update.callback_query.data[len(CONFIRM_DECLINE_BROADCAST):]
    entities_for_celery = update.callback_query.message.to_dict().get('entities')
    entities = update.callback_query.message.entities
    text = update.callback_query.message.text
    admin_text = text

    context.bot.edit_message_text(
        text=admin_text,
        chat_id=update.callback_query.message.chat_id,
        message_id=update.callback_query.message.message_id,
        entities=None if broadcast_decision == CONFIRM_BROADCAST else entities
    )
