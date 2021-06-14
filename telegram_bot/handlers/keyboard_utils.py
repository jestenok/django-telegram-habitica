from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram_bot.models import User

from telegram_bot.handlers.manage_data import SECRET_LEVEL_BUTTON, CONFIRM_DECLINE_BROADCAST, CONFIRM_BROADCAST, \
    DECLINE_BROADCAST, COMPLETE_TASK
from telegram_bot.handlers.static_text import github_button_text, secret_level_button_text, confirm_broadcast, \
    decline_broadcast


def keyboard(update, context):
    u = User.get_user(update, context)

    context.bot.send_message(
        chat_id=u.user_id, text=('Привет! Я менеджер задач. Нажми на кнопку /task и введи описание задачи '
                                 'одним сообщением. При успешном выполнении или изменении статуса, будет '
                                 'отправлено уведомление.'),
        reply_markup=ReplyKeyboardMarkup([
            [KeyboardButton(text="/task"), KeyboardButton(text="/admin"), KeyboardButton(text="/stats")],
        ], resize_keyboard=True),  # 'False' will make this button appear on half screen (become very large). Likely,
        # it will increase click conversion but may decrease UX quality.
    )


def make_keyboard_for_task_command(task_number):
    buttons = [[InlineKeyboardButton('Завершить', callback_data=f'{COMPLETE_TASK}{task_number}')]]

    return InlineKeyboardMarkup(buttons)


def keyboard_confirm_decline_broadcasting():
    buttons = [[
        InlineKeyboardButton(confirm_broadcast, callback_data=f'{CONFIRM_DECLINE_BROADCAST}{CONFIRM_BROADCAST}'),
        InlineKeyboardButton(decline_broadcast, callback_data=f'{CONFIRM_DECLINE_BROADCAST}{DECLINE_BROADCAST}')
    ]]

    return InlineKeyboardMarkup(buttons)

