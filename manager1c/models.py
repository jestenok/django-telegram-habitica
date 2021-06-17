import datetime

from django.db import models


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