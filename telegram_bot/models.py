import datetime

from django.db import models
from telegram_bot import utils


class User(models.Model):
    user_id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=32, null=True, blank=True)
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256, null=True, blank=True)
    language_code = models.CharField(max_length=8, null=True, blank=True, help_text="Telegram client's lang")
    deep_link = models.CharField(max_length=64, null=True, blank=True)

    is_blocked_bot = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)

    is_admin = models.BooleanField(default=False)
    is_moderator = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    waiting_for_input = models.BooleanField(default=False)
    waiting_for_announcement = models.BooleanField(default=False)

    anime = models.BooleanField(default=False)
    anime_id = models.CharField(max_length=10, null=True, blank=True)
    anime_code = models.CharField(max_length=50, null=True, blank=True)
    anime_token = models.CharField(max_length=50, null=True, blank=True)
    anime_refresh_token = models.CharField(max_length=50, null=True, blank=True)
    anime_username = models.CharField(max_length=32, null=True, blank=True)
    anime_password = models.CharField(max_length=32, null=True, blank=True)


    def __str__(self):
        return f'@{self.username}' if self.username is not None else f'{self.user_id}'

    @classmethod
    def get_user_and_created(cls, update, context):
        """ python-telegram_bot-bot's Update, Context --> User instance """
        data = utils.extract_user_data_from_update(update)
        u, created = cls.objects.update_or_create(user_id=data["user_id"], defaults=data)

        if created:
            if context is not None and context.args is not None and len(context.args) > 0:
                payload = context.args[0]
                if str(payload).strip() != str(data["user_id"]).strip():  # you can't invite yourself
                    u.deep_link = payload
                    u.save()

        return u, created

    @classmethod
    def get_user(cls, update, context):
        u, _ = cls.get_user_and_created(update, context)
        return u

    @classmethod
    def get_user_by_username_or_user_id(cls, string):
        """ Search user in DB, return User or None if not found """
        username = str(string).replace("@", "").strip().lower()
        if username.isdigit():  # user_id
            return cls.objects.filter(user_id=int(username)).first()
        return cls.objects.filter(username__iexact=username).first()

    def invited_users(self):  # --> User queryset 
        return User.objects.filter(deep_link=str(self.user_id), created_at__gt=self.created_at)


class Logs(models.Model):
    date = models.DateTimeField()
    log_type = models.CharField(max_length=50, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(null=True)

    @classmethod
    def log(cls, log_type, user, text):
        date = datetime.datetime.now()
        cls.objects.create(date=date, log_type=log_type, user=user, text=text)


class UserMessages(models.Model):
    date = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(null=True)

    @classmethod
    def log(cls, user, text):
        date = datetime.datetime.now()
        cls.objects.create(date=date, user=user, text=text)


class Message(models.Model):
    doc_type = models.CharField(max_length=255, null=True, blank=True)
    doc_number = models.CharField(max_length=255, null=True, blank=True)
    doc_date = models.DateTimeField(null=True, blank=True)

    text = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"user: {self.doc_type}, task: {self.doc_number}"


    @classmethod
    def message_update_or_create(cls, doc_type='', doc_number=0, doc_date=datetime.datetime.now(), text=''):
        data = {'doc_type': doc_type,
                'doc_number': doc_number,
                'doc_date': doc_date,
                'text': text,
                }
        message, created = cls.objects.update_or_create(doc_type=data['doc_type'], doc_number=['doc_number'], defaults=data)
        return message, created


    @classmethod
    def message_get(cls, doc_number):
        message = cls.objects.get(doc_number=doc_number)
        return message


class Task(models.Model):
    task_number = models.AutoField(primary_key=True)
    user_telegram_id = models.ForeignKey(User, on_delete=models.CASCADE)
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
                'startDate': datetime.datetime.strptime(task.createdAt, '%Y-%m-%dT%H:%M:%S.%fZ'),
                'date': datetime.datetime.now(),
                'completed': task.completed}
        if user_telegram_id != '':
            data['user_telegram_id'] = user_telegram_id

        task, created = cls.objects.update_or_create(id=data['id'], defaults=data)
        return task, created


    @classmethod
    def task_get(cls, task_number):
        task = cls.objects.get(task_number=task_number)
        return task
