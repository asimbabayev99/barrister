# Generated by Django 3.0.3 on 2020-11-26 13:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0046_merge_20201031_1644'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='contact',
            name='home_contac_user_id_83d972_idx',
        ),
        migrations.RemoveField(
            model_name='contact',
            name='name',
        ),
        migrations.AddField(
            model_name='contact',
            name='barrister',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contacts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='contact',
            name='first_name',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='contact',
            name='last_name',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='contact',
            name='status',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
        migrations.AddIndex(
            model_name='contact',
            index=models.Index(fields=['user'], name='home_contac_user_id_970c0e_idx'),
        ),
    ]
