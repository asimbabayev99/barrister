# Generated by Django 2.2.3 on 2020-05-04 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_task_media_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('completed', 'completed'), ('in progress', 'in progress')], default='in progress', max_length=32),
        ),
    ]
