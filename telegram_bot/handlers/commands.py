import datetime
import re

import requests
from django.utils import timezone

import telegram
from .anime import search, anime_headers
from manager.config import TG_API_KEY, anime_client_id
from telegram_bot.utils import extract_user_data_from_update
from telegram_bot.models import User, UserMessages, Task, Message
from . import static_text, parser, habitica as hcmd
from .keyboard_utils import (make_keyboard_for_task_command,
                                                  keyboard_confirm_decline_broadcasting,
                                                  make_keyboard_for_anime_search)


def text_message(update, context):
    u = User.get_user(update, context)
    text = update.message.caption if update.message.caption else update.message.text
    UserMessages.log(u,text)
    answer = static_text.message_answer(text)
    if u.waiting_for_input:
        User.objects.filter(user_id=u.user_id).update(waiting_for_input=False)
        username = f'@{u.username}' if u.username else u.first_name
        bd_task, created = hcmd.task_create(u.user_id, username, text)
        answer_text = static_text.task_text(bd_task)

        receivers = ['1021912706', u.user_id]
        for receiver in receivers:
            if update.message.caption:
                photo = update.message.photo[len(update.message.photo) - 1]
                bot.send_photo(chat_id=receiver,
                               photo=photo.file_id,
                               caption=answer_text,
                               parse_mode=telegram.ParseMode.HTML,
                               reply_markup=make_keyboard_for_task_command(bd_task.task_number))
            else:
                bot.send_message(chat_id=receiver,
                                 text=answer_text,
                                 parse_mode=telegram.ParseMode.HTML,
                                 reply_markup=make_keyboard_for_task_command(bd_task.task_number))

    elif u.waiting_for_announcement:
        User.objects.filter(user_id=u.user_id).update(waiting_for_announcement=False)
        for obj in User.objects.all():
            bot.send_message(obj.user_id, text)
    elif answer:
        return update.message.reply_text(answer)
    elif u.anime:
        obj = search(u, text)
        update.message.reply_text(f"Список аниме по запросу {text}:", parse_mode=telegram.ParseMode.HTML)
        i=1
        for item in obj:
            datetime_object = datetime.datetime.strptime(item.aired_on, '%Y-%m-%d')
            text = f'{i}. <a href="https://shikimori.one{item.url}">{item.russian}</a>' \
                   f'\n({datetime_object.strftime("%d.%m.%Y")})'
            bot.send_photo(u.user_id,
                           photo=requests.get(f"https://shikimori.one{item.image.original}", headers=anime_headers()).content,
                           reply_markup=make_keyboard_for_anime_search(item.id),
                           caption=text,
                           parse_mode=telegram.ParseMode.HTML)
            i += 1


def get_tasks(update, context):
    update.message.reply_text(parser.parse())


def send_message_to_admin(text):
    bot.send_message('1021912706', text)


def task(update, context):
    u = User.get_user(update, context)
    User.objects.filter(user_id=u.user_id).update(waiting_for_input=True)
    context.bot.send_message(chat_id=u.user_id, text='Введите описание задачи',
                             reply_markup=telegram.ReplyKeyboardMarkup([[telegram.KeyboardButton(text="/task")],],
                                                                       resize_keyboard=True))


def mylist(update, context):
    u = User.get_user(update, context)
    if u.anime:
        obj = search(u, planned=True)
        text = f"Список запланированных аниме:"

        i = 1
        for item in obj:
            datetime_object = datetime.datetime.strptime(item.aired_on, '%Y-%m-%d')
            text += f'\n{i}. <a href="https://shikimori.one{item.url}">{item.russian}</a>' \
                   f' ({datetime_object.strftime("%d.%m.%Y")})'
            i += 1

        update.message.reply_text(text, parse_mode=telegram.ParseMode.HTML,
                                  disable_web_page_preview=True)


def anime(update, context):
    u = User.get_user(update, context)
    if u.anime:
        User.objects.filter(user_id=u.user_id).update(anime=False)
        text = "Режим анимешника деактивирован"
    else:
        text = f'Необходимо разрешить доступ по ' \
               f'<a href="https://shikimori.one/oauth/authorize?client_id={anime_client_id}&' \
               f'redirect_uri=https%3A%2F%2Fjestenok.ru%2Fanime%3Fuser_id%3D{u.user_id}' \
               f'&response_type=code&scope=user_rates">ссылке</a>'

    context.bot.send_message(chat_id=u.user_id, text=text,
                             reply_markup=telegram.ReplyKeyboardMarkup([[telegram.KeyboardButton(text="/task")],],
                                                                       resize_keyboard=True),
                             parse_mode=telegram.ParseMode.HTML)


def yesterday_tasks(update, context):
    u = User.get_user(update, context)
    if not u.is_admin:
        update.message.reply_text('Недостаточно прав!')
        return
    delimiter = '\n\n'
    if datetime.date.weekday(datetime.date.today()) == 0:
        answer_text = f'Список задач за пятницу:'
        tasks = Task.objects.all().filter(date__range=[datetime.date.today() + datetime.timedelta(days=-3),
                                                       datetime.date.today()])
    else:
        answer_text = f'Список задач за вчерашний день:'
        tomorrow = datetime.date.today() + datetime.timedelta(days=-1)
        tasks = Task.objects.all().filter(date__contains=tomorrow) #date__range=["2011-01-01", "2011-01-31"]
    for t in tasks:
        if t.completed:
            compleeted = '✅'
        else:
            compleeted = '❌'
        text = t.text.replace(' # ', f'\n{compleeted} ')
        answer_text += f'{delimiter}{text}'
    update.message.reply_text(answer_text)


def nowdays_tasks(update, context):
    u = User.get_user(update, context)
    if not u.is_admin:
        update.message.reply_text('Недостаточно прав!')
        return
    delimiter = '\n\n'
    answer_text = f'Список задач на сегодня:'
    tasks = Task.objects.all().filter(completed=False)
    for t in tasks:
        text = t.text.replace(' # ', f'\n')
        answer_text += f'{delimiter}{text}'
    update.message.reply_text(answer_text)


def announcement(update, context):
    u = User.get_user(update, context)
    if not u.is_admin:
        update.message.reply_text('Недостаточно прав!')
        return
    User.objects.filter(user_id=u.user_id).update(waiting_for_announcement=True)
    update.message.reply_text('Введите описание объявления')


def habitica_task_compleeted(task) -> object:
    text = static_text.task_text(task)
    bot.send_message(task.user_telegram_id, text, parse_mode=telegram.ParseMode.HTML)


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


bot = telegram.Bot(TG_API_KEY)
