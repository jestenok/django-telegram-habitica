import requests
from manager import config
import json
from collections import namedtuple
from telegram_bot.models import Task


api_user = config.HABITICA_API_USER
api_key = config.HABITICA_API_KEY

headers = {'x-api-user': api_user, 'x-api-key': api_key}


def get_object_from_request(json_data):
    json_data = json.dumps(json_data).replace('_id', 'id')
    obj = json.loads(json_data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    return obj


def task_create(user_telegram, username, text, notes=''):
    data = {'text': f'{username} # {text}', 'notes': notes, 'type': 'todo'}
    r = requests.post(url='https://habitica.com/api/v3/tasks/user', headers=headers, data=data)
    task = get_object_from_request(r.json())
    return Task.task_update_or_create(task.data, user_telegram)


def task_update(task):
    r = requests.post(url=f'https://habitica.com/api/v3/tasks/{task.id}/score/up', headers=headers)


def task_compleeted(json_data):
    from telegram_bot.handlers.commands import habitica_task_compleeted
    task = namedtuple("ObjectName", json_data['task'].keys())(*json_data['task'].values())
    task_db, _ = Task.task_update_or_create(task)
    habitica_task_compleeted(task_db)
