# Generated by Django 2.2.3 on 2020-04-04 10:32

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0021_auto_20200404_1424'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='seriya_type',
            field=models.CharField(choices=[('AZE', 'AZE'), ('AA', 'AA')], default=django.utils.timezone.now, max_length=5),
            preserve_default=False,
        ),
    ]