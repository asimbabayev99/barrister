# Generated by Django 2.2.3 on 2020-09-17 10:53

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Code',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('number', models.IntegerField()),
                ('active', models.BooleanField(default=True)),
                ('content', ckeditor.fields.RichTextField()),
            ],
        ),
    ]
