import requests
from manager import config
import json
from collections import namedtuple
from telegram_bot.models import Message
from .commands import bot_send_message


def process_1c_event(json_data):
    message = namedtuple("ObjectName", json_data.keys())(*json_data.values())
    Message.message_update_or_create(message.doc_type,
                                     message.doc_number,
                                     message.doc_date,
                                     message.text)
    text = f"{message.doc_type}" \
           f"{message.doc_number} от {message.doc_date}" \
           f"{message.text}"

    bot_send_message(message.user_id, json_data)
