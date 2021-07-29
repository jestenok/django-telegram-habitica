import requests
from manager import config
import json
from collections import namedtuple
from telegram_bot.models import Message
from .commands import send_message_to_admin


def process_1c_event(json_data):
    message = namedtuple("ObjectName", json_data.keys())(*json_data.values())
    Message.message_update_or_create(doc_type=message.doc_type, doc_number=message.doc_number,
                                     doc_date=message.doc_date, text=message.text)
    send_message_to_admin(json_data)