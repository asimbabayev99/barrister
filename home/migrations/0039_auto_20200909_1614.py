# Generated by Django 2.2.3 on 2020-09-09 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0038_auto_20200909_1250'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='completed',
        ),
    ]