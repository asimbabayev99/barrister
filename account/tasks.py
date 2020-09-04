from __future__ import absolute_import, unicode_literals
from celery import shared_task
from datetime import timezone, datetime

from django.core.files.base import ContentFile
import imaplib
import base64
import os
import email
import mailparser
from dateutil import parser
import bs4
# models
from account.models import CustomUser
from home.models import EmailAccount, Email, Attachment


def GenerateOAuth2String(email, access_token, base64_encode=True):
  """Generates an IMAP OAuth2 authentication string.

  See https://developers.google.com/google-apps/gmail/oauth2_overview

  Args:
    username: the username (email address) of the account to authenticate
    access_token: An OAuth2 access token.
    base64_encode: Whether to base64-encode the output.

  Returns:
    The SASL argument for the OAuth2 mechanism.
  """
  auth_string = 'user=%s\1auth=Bearer %s\1\1' % (email, access_token)
  if base64_encode:
    auth_string = base64.b64encode(auth_string)
  return auth_string











@shared_task(name = "synchronize_mail")
def synchronize_mail(email_address, token):
    print("start to synchronize mail")
    server = 'imap.yandex.ru'
    mail = imaplib.IMAP4_SSL(server)
    print(email_address,token,GenerateOAuth2String(email_address,token,base64_encode=False))
    mail.authenticate('XOAUTH2',lambda x: GenerateOAuth2String(email_address,token,base64_encode=False))
    mail_folders = ['Inbox','Drafts','Sent','Trash']
    user = EmailAccount.objects.get(email=email_address).user

    # loop th rough mail folders
    for folder in mail_folders:
        mail.select("{0}".format(folder))
        print(folder)
        type, data = mail.search(None, 'ALL')

        # loop throught emails
        for num in data[0].split():
            
            num = num.decode()
            typ, data = mail.fetch(num, '(RFC822)' )
            raw_email = data[0][1]
            # converts byte literal to string removing b''
          
            email_message = mailparser.parse_from_bytes(raw_email)
            subject = email_message.subject
            sender = email_message.from_[0][1]
            receiver = email_message.to[0][1]
            date = email_message.date
            print(subject)
            # timestamp = email.utils.parsedate_tz(date)

            new_email, created = Email.objects.get_or_create(folder=folder,user=user,num=num, sender=sender, receiver=receiver, date=date)
            
            print("folder=", folder, "num=", num, "sender=", sender, "receiver=", receiver, "date=", date)
            if  not created:
                print("already created")
                continue
            new_email.subject = subject
            content = email_message.text_html[0] if email_message.text_html != [] else ""
            new_email.content = content
            new_email.save()
            if email_message.attachments is not None:
              for i in email_message.attachments:
                attachment = Attachment(name=i['filename'],email=new_email)
                attachment.file.save(i['filename'],ContentFile(base64.b64decode(i['payload'])))
                attachment.save()

    



    return "email synchronized"



@shared_task(name = "check_mails")
def check_mails():

    return "completed doing tasks"



