# Generated by Django 2.2.3 on 2020-04-04 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0022_customuser_seriya_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='adress',
            field=models.CharField(max_length=256, null=True),
        ),
    ]
