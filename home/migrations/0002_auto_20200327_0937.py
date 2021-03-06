# Generated by Django 2.2.3 on 2020-03-27 05:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('description', models.CharField(max_length=256)),
                ('location', models.CharField(max_length=256)),
                ('completed', models.BooleanField(default=False)),
                ('frequency', models.CharField(choices=[('Fixed', 'fixed'), ('Daily', 'daily'), ('Weekly', 'weekly'), ('Monthly', 'monthly'), ('Yearly', 'yearly')], max_length=32)),
                ('frequency_count', models.IntegerField(default=1)),
                ('date', models.DateField(auto_now=True)),
                ('from_time', models.TimeField(auto_now=True)),
                ('to_time', models.TimeField(auto_now=True)),
                ('remind_me', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='EventCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.DeleteModel(
            name='Task',
        ),
        migrations.DeleteModel(
            name='TaskCategory',
        ),
        migrations.AddField(
            model_name='event',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.EventCategory'),
        ),
        migrations.AddField(
            model_name='event',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
