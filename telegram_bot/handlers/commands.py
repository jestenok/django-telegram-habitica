import datetime
import re

import telegram
from django.core.management.utils import parse_apps_and_model_labels
from django.utils import timezone

from telegram_bot.handlers import static_text
from telegram_bot.handlers.keyboard_utils import (make_keyboard_for_start_command,
                                                  keyboard_confirm_decline_broadcasting)
from telegram_bot.handlers.utils import handler_logging
from telegram_bot.models import User
from telegram_bot.utils import extract_user_data_from_update


def text_message(update, context):
    from mng_habitica.handlers import commands as hcmd

    u = User.get_user(update, context)
    text = update.message.text

    answer = message_answer(text)
    if answer != '':
        return update.message.reply_text(answer)

    if u.waiting_for_input:
        User.objects.filter(user_id=u.user_id).update(waiting_for_input=False)
        bd_task, created = hcmd.task_create(u.user_id, u.username, text)

        reply_text = f'Задача № {bd_task.task_number}' \
                     f'<pre language="python>">{bd_task.text}</pre> Принята в работу!\n' \
                     f'При ее завершении будет отправлено уведомление!'

        update.message.reply_text(reply_text, parse_mode=telegram.ParseMode.HTML)


def message_answer(question):
    answers = {'привет': 'Привет солнышко тьмок :*',
               'спокойной ночи': 'Сладких снов :*', }

    return answers[question.lower()]


@handler_logging()
def command_start(update, context):
    u, created = User.get_user_and_created(update, context)

    if created:
        text = static_text.start_created.format(first_name=u.first_name)
    else:
        text = static_text.start_not_created.format(first_name=u.first_name)

    update.message.reply_text(text=text + 'kek',
                              reply_markup=make_keyboard_for_start_command())


def task(update, context):
    u = User.get_user(update, context)
    User.objects.filter(user_id=u.user_id).update(waiting_for_input=True)
    context.bot.send_message(chat_id=u.user_id, text='Введите описание задачи')


def stats(update, context):
    u = User.get_user(update, context)
    if not u.is_admin:
        return

    text = f"""
*Users*: {User.objects.count()}
*24h active*: {User.objects.filter(updated_at__gte=timezone.now() - datetime.timedelta(hours=24)).count()}
    """

    return update.message.reply_text(
        text,
        parse_mode=telegram.ParseMode.MARKDOWN,
        disable_web_page_preview=True,
    )


def broadcast_command_with_message(update, context):
    """ Type /broadcast <some_text>. Then check your message in Markdown format and broadcast to users."""
    u = User.get_user(update, context)
    user_id = extract_user_data_from_update(update)['user_id']

    if not u.is_admin:
        text = static_text.broadcast_no_access
        markup = None

    else:
        text = f"{update.message.text.replace(f'{static_text.broadcast_command} ', '')}"
        markup = keyboard_confirm_decline_broadcasting()

    try:
        context.bot.send_message(
            text=text,
            chat_id=user_id,
            parse_mode=telegram.ParseMode.MARKDOWN,
            reply_markup=markup
        )
    except telegram.error.BadRequest as e:
        place_where_mistake_begins = re.findall(r"offset (\d{1,})$", str(e))
        text_error = static_text.error_with_markdown
        if len(place_where_mistake_begins):
            text_error += f"{static_text.specify_word_with_error}'{text[int(place_where_mistake_begins[0]):].split(' ')[0]}'"
        context.bot.send_message(
            text=text_error,
            chat_id=user_id
        )
