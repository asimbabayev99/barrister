# Generated by Django 2.2.3 on 2020-04-01 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0012_profile_work_summary'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='facebook_link',
            field=models.URLField(null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='google_link',
            field=models.URLField(null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='linkedin_link',
            field=models.URLField(null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='twitter_link',
            field=models.URLField(null=True),
        ),
    ]
