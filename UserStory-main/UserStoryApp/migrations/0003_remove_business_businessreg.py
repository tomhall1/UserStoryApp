# Generated by Django 2.1.15 on 2022-11-16 09:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UserStoryApp', '0002_auto_20221116_1126'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='business',
            name='businessReg',
        ),
    ]
