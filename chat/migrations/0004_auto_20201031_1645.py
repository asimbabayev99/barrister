# Generated by Django 2.2.3 on 2020-10-31 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_attachment_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachment',
            name='file',
            field=models.FileField(null=True, upload_to='chat/attachments/'),
        ),
    ]