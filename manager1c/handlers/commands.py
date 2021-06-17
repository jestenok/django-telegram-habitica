import requests
from manager import config
import json
from collections import namedtuple
from manager1c.models import Message
from telegram_bot.handlers.commands import send_message_to_admin


def process_1c_event(json_data):
    message = namedtuple("ObjectName", json_data.keys())(*json_data.values())
    Message.message_update_or_create(doc_type=message.doc_type, doc_number=message.doc_number,
                                     doc_date=message.doc_date, text=message.text)
    send_message_to_admin(json_data)