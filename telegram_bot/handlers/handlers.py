import telegram
from telegram_bot.handlers.habitica import task_update
from telegram_bot.handlers.manage_data import CONFIRM_DECLINE_BROADCAST, CONFIRM_BROADCAST, COMPLETE_TASK, PLANNED
from telegram_bot.handlers.static_text import task_text
from telegram_bot.handlers.commands import bot
from telegram_bot.models import User, Task
from telegram_bot.utils import extract_user_data_from_update
from telegram_bot.handlers.anime import change_status


def comlete_task(update, context):
    user_id = extract_user_data_from_update(update)['user_id']
    task_number = update.callback_query.data[len(COMPLETE_TASK):]
    task = Task.task_get(task_number)
    text = task_text(task)
    task_update(task)

    if update.callback_query.message.caption:
        bot.edit_message_caption(
            caption=text,
            chat_id=user_id,
            message_id=update.callback_query.message.message_id,
            parse_mode=telegram.ParseMode.HTML)
    else:
        context.bot.edit_message_text(
            text=text,
            chat_id=user_id,
            message_id=update.callback_query.message.message_id,
            parse_mode=telegram.ParseMode.HTML)


def anime_action(update, context):
    u = User.get_user(update, context)
    text = update.callback_query.data
    caption = update.callback_query.message.caption

    url = update.callback_query.message.caption_entities[0].url
    id = url[url.find("animes/") + 7:url.find("-")]

    text_for_link = caption[caption.find(". ") + 2:caption.find("(")]
    caption = caption.replace(text_for_link, f'<a href="{url}">{text_for_link}</a>')

    if text.find(PLANNED) != -1 :
        change_status(u, id, "planned")
        bot.edit_message_caption(
            caption=caption + "\n🕒 Запланировано",
            chat_id=u.user_id,
            message_id=update.callback_query.message.message_id,
            parse_mode=telegram.ParseMode.HTML)
    else:
        change_status(u, id, "completed")
        bot.edit_message_caption(
            caption=caption + "\n✅ Просмотрено",
            chat_id=u.user_id,
            message_id=update.callback_query.message.message_id,
            parse_mode=telegram.ParseMode.HTML)


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
        entities=None if broadcast_decision == CONFIRM_BROADCAST else entities)
