# Generated by Django 3.0.3 on 2020-12-02 07:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0048_auto_20201201_1342'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contact',
            old_name='adress',
            new_name='address',
        ),
    ]