# Generated by Django 2.2.3 on 2020-10-19 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('template', models.FileField(upload_to='documents')),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
