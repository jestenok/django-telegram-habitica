from datetime import datetime

from django.db import models


class Task(models.Model):
    task_number = models.AutoField(primary_key=True)
    user_telegram_id = models.IntegerField(null=True, blank=True)
    id = models.CharField(max_length=255, null=True, blank=True)

    completed = models.BooleanField(null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    type_choices = [('habit', 'habit'),
                    ('daily', 'daily'),
                    ('todo', 'todo'),
                    ('reward', 'reward')]
    type = models.CharField(max_length=255, choices= type_choices, null=True, blank=True)

    tags = models.CharField(max_length=255, null=True, blank=True)
    alias = models.CharField(max_length=255, null=True, blank=True)
    attribute = models.CharField(max_length=255, null=True, blank=True)
    collapseChecklist = models.BooleanField(null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)

    priority_choices = [(0.1, 'Trivial'),
                        (1, 'Easy'),
                        (1.5, 'Medium'),
                        (2, 'Hard')]
    priority = models.IntegerField(choices=priority_choices, null=True, blank=True)

    reminders = models.CharField(max_length=255, null=True, blank=True)

    frequency_choices = [('daily', 'daily'),
                        ('weekly', 'weekly'),
                        ('monthly', 'monthly'),
                        ('yearly', 'yearly')]
    frequency = models.CharField(max_length=255, choices=frequency_choices,null=True, blank=True)

    repeat = models.CharField(max_length=255, null=True, blank=True)
    everyX = models.IntegerField(null=True, blank=True)
    streak = models.IntegerField(null=True, blank=True)
    daysOfMonth = models.IntegerField(null=True, blank=True)
    weeksOfMonth = models.IntegerField(null=True, blank=True)
    startDate = models.DateTimeField(null=True, blank=True)
    up = models.BooleanField(null=True, blank=True)
    down = models.BooleanField(null=True, blank=True)
    value = models.IntegerField(null=True, blank=True)
    image = models.ImageField(upload_to=f'images/', null=True, blank=True)

    def __str__(self):
        return f"user: {self.user_telegram_id}, task: {self.text}"


    @classmethod
    def task_update_or_create(cls, task, user_telegram_id=''):
        data = {'id': task.id,
                'type': task.type,
                'text': task.text,
                'notes': task.notes,
                'date': datetime.strptime(task.createdAt, '%Y-%m-%dT%H:%M:%S.%fZ'),
                'completed': task.completed}
        if user_telegram_id != '':
            data['user_telegram_id'] = user_telegram_id

        task, created = cls.objects.update_or_create(id=data['id'], defaults=data)
        return task, created


    @classmethod
    def task_get(cls, task_number):
        task = cls.objects.get(task_number=task_number)
        return task
