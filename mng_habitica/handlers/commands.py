import requests
from manager import config
import json
from collections import namedtuple
from mng_habitica.models import Task
from telegram_bot.handlers.dispatcher import habitica_task_compleeted

api_user = config.HABITICA_API_USER
api_key = config.HABITICA_API_KEY

headers = {'x-api-user': api_user, 'x-api-key': api_key}


def get_object_from_request(json_data):
    json_data = json.dumps(json_data).replace('_id', 'id')
    obj = json.loads(json_data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    return obj


def task_create(user_telegram_id, username, text, notes=''):
    data = {'text': username + ' # ' + text, 'notes': notes, 'type': 'todo'}
    r = requests.post(url='https://habitica.com/api/v3/tasks/user', headers=headers, data=data)
    task = get_object_from_request(r.json())
    return Task.task_update_or_create(task.data, user_telegram_id)


def task_compleeted(json_data):
    task = namedtuple("ObjectName", json_data['task'].keys())(*json_data['task'].values())
    task_db, _ = Task.task_update_or_create(task)
    habitica_task_compleeted(task_db)


