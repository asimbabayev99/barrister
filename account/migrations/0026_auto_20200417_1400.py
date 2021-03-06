# Generated by Django 2.2.3 on 2020-04-17 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0025_auto_20200413_1344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(null=True, upload_to='profile'),
        ),
        migrations.AddIndex(
            model_name='award',
            index=models.Index(fields=['profile'], name='account_awa_profile_a889fc_idx'),
        ),
        migrations.AddIndex(
            model_name='educationandworkexperience',
            index=models.Index(fields=['profile'], name='account_edu_profile_0e79dc_idx'),
        ),
        migrations.AddIndex(
            model_name='jobcategory',
            index=models.Index(fields=['slug'], name='account_job_slug_3b4f0e_idx'),
        ),
        migrations.AddIndex(
            model_name='profile',
            index=models.Index(fields=['user'], name='account_pro_user_id_90d36a_idx'),
        ),
        migrations.AddIndex(
            model_name='role',
            index=models.Index(fields=['name'], name='account_rol_name_fa94e9_idx'),
        ),
        migrations.AddIndex(
            model_name='skill',
            index=models.Index(fields=['profile'], name='account_ski_profile_4ede4f_idx'),
        ),
    ]
