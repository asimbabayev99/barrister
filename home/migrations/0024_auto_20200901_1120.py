# Generated by Django 2.2.3 on 2020-09-01 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0023_auto_20200827_1522'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
