# Generated by Django 2.2.3 on 2020-08-27 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0022_auto_20200827_1521'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='client',
            index=models.Index(fields=['user'], name='home_client_user_id_fc6b54_idx'),
        ),
    ]
