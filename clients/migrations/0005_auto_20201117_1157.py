# Generated by Django 3.0.3 on 2020-11-17 07:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0004_auto_20201112_1158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='case',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='case', to='clients.Client'),
        ),
    ]
