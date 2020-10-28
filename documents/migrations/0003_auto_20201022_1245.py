# Generated by Django 2.2.3 on 2020-10-22 08:45

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0002_auto_20201020_1035'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='form_html',
            field=models.TextField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='document',
            name='form_js',
            field=models.TextField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]