# Generated by Django 2.2.3 on 2020-04-02 13:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0016_auto_20200402_1127'),
    ]

    operations = [
        migrations.RenameField(
            model_name='educationandworkexperience',
            old_name='to_time',
            new_name='end',
        ),
        migrations.RenameField(
            model_name='educationandworkexperience',
            old_name='from_time',
            new_name='start',
        ),
    ]
