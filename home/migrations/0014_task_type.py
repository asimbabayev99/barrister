# Generated by Django 2.2.3 on 2020-05-04 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0013_auto_20200504_1329'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='type',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
    ]