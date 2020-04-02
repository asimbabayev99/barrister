# Generated by Django 2.2.3 on 2020-04-02 07:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0015_auto_20200402_1119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='award',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='awards', to='account.Profile'),
        ),
        migrations.AlterField(
            model_name='educationandworkexperience',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='experiences', to='account.Profile'),
        ),
        migrations.AlterField(
            model_name='skill',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='skills', to='account.Profile'),
        ),
    ]
