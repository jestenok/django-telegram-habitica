# Generated by Django 3.2.4 on 2021-06-17 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager1c', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='doc_number',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
