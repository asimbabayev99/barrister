# Generated by Django 2.2.3 on 2020-09-07 08:07

import django.core.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0029_auto_20200907_1202'),
    ]

    operations = [
        migrations.RenameField(
            model_name='eventcategory',
            old_name='color',
            new_name='bg_color',
        ),
        migrations.AddField(
            model_name='eventcategory',
            name='text_color',
            field=models.CharField(blank=True, max_length=16, null=True),
        ),
        migrations.AlterField(
            model_name='eventcategory',
            name='icon',
            field=models.FileField(default=django.utils.timezone.now, upload_to='event-categories/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['svg'])]),
            preserve_default=False,
        ),
    ]