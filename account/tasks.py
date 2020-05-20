from __future__ import absolute_import, unicode_literals
from celery import shared_task
from datetime import timezone

# models
from account.models import CustomUser


@shared_task(name = "synchronize_mail")
def synchronize_mail(user_id, email, password):
    
    return "email synchronized"



@shared_task(name = "check_mails")
def check_mails():

    return "completed doing tasks"



