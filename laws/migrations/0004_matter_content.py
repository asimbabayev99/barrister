# Generated by Django 2.2.3 on 2020-09-28 08:35

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('laws', '0003_law_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='matter',
            name='content',
            field=ckeditor.fields.RichTextField(default=1),
            preserve_default=False,
        ),
    ]