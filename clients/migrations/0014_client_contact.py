# Generated by Django 3.0.3 on 2020-12-01 09:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0047_auto_20201126_1712'),
        ('clients', '0013_notes_barrister'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='contact',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='home.Contact'),
        ),
    ]
