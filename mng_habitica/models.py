from datetime import datetime

from django.db import models


class Task(models.Model):
    task_number = models.AutoField(primary_key=True)
    user_telegram_id = models.IntegerField(null=True)
    id = models.CharField(max_length=255, null=True)

    text = models.TextField(null=True)
    notes = models.TextField(null=True)

    type_choices = [('habit', 'habit'),
                    ('daily', 'daily'),
                    ('todo', 'todo'),
                    ('reward', 'reward')]
    type = models.CharField(max_length=255, choices= type_choices, null=True)

    tags = models.CharField(max_length=255, null=True)
    alias = models.CharField(max_length=255, null=True)
    attribute = models.CharField(max_length=255, null=True)
    collapseChecklist = models.BooleanField(null=True)
    date = models.DateTimeField(null=True)

    priority_choices = [(0.1, 'Trivial'),
                        (1, 'Easy'),
                        (1.5, 'Medium'),
                        (2, 'Hard')]
    priority = models.IntegerField(choices=priority_choices, null=True)

    reminders = models.CharField(max_length=255, null=True)

    frequency_choices = [('daily', 'daily'),
                        ('weekly', 'weekly'),
                        ('monthly', 'monthly'),
                        ('yearly', 'yearly')]
    frequency = models.CharField(max_length=255, choices=frequency_choices,null=True)

    repeat = models.CharField(max_length=255, null=True)
    everyX = models.IntegerField(null=True)
    streak = models.IntegerField(null=True)
    daysOfMonth = models.IntegerField(null=True)
    weeksOfMonth = models.IntegerField(null=True)
    startDate = models.DateTimeField(null=True)
    up = models.BooleanField(null=True)
    down = models.BooleanField(null=True)
    value = models.IntegerField(null=True)

    def __str__(self):
        return f"user: {self.user_telegram_id}, task: {self.text}"


    @classmethod
    def task_update_or_create(cls, task, user_telegram_id=''):
        data = {'id': task.id,
                'type': task.type,
                'text': task.text,
                'notes': task.notes,
                'date': datetime.strptime(task.createdAt, '%Y-%m-%dT%H:%M:%S.%fZ')}
        if user_telegram_id != '':
            data['user_telegram_id'] = user_telegram_id

        task, created = cls.objects.update_or_create(id=data['id'], defaults=data)
        return task, created





#
# def fill_receiver_from_source(source, receiver):
#     for r in receiver:
#         for s in source:
#             if s in receiver:
#                 receiver[s] = source[s]