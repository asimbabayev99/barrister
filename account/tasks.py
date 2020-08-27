from __future__ import absolute_import, unicode_literals
from celery import shared_task
from datetime import timezone, datetime

from django.core.files.base import ContentFile
import imaplib
import base64
import os
import email


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
    mail.authenticate('XOAUTH',lambda x: GenerateOAuth2String(email_address,token))
    mail_folders = ['Inbox',]
    # loop through mail folders
    for folder in mail_folders:
        mail.select(folder)
        type, data = mail.search(None, 'ALL')
        mail_ids = data[0]
        id_list = mail_ids.split()

        # loop throught emails
        for num in data[0].split():
            print(num)
            typ, data = mail.fetch(num, '(RFC822)' )
            raw_email = data[0][1]
            # converts byte literal to string removing b''
            
            raw_email_string = raw_email.decode('utf-8')
            email_message = email.message_from_string(raw_email_string)

            subject = email_message['Subject']
            subject = email.header.make_header(email.header.decode_header(subject))

            sender = email_message['From'].split()
            sender = sender[len(sender) - 1].replace('<', '').replace('>', '')

            receiver = email_message['To'].split()
            receiver = receiver[len(receiver) - 1].replace('<', '').replace('>', '')

            date = email_message['Date']
            date = datetime.strptime(date, '%a, %d %b %Y %X %z')
            # timestamp = email.utils.parsedate_tz(date)

            new_email, created = Email.objects.get_or_create(user=user, folder=folder, num=num, sender=sender, receiver=receiver, date=date)
            
            print("folder=", folder, "num=", num, "sender=", sender, "receiver=", receiver, "date=", date)
            if not created:
                print("already created")
                continue

            # downloading attachments
            for part in email_message.walk():
                if part.get_content_maintype() == 'text':
                    content = part.get_payload(decode=True)
                    new_email.content = content
                    new_email.save()

                if part.get_content_maintype() == 'multipart':
                    continue
                if part.get('Content-Disposition') is None:
                    continue

                fileName = part.get_filename()
                fileName = email.header.make_header(email.header.decode_header(fileName))

                if bool(fileName):
                    attachment = Attachment(email=new_email, name=str(fileName))
                    attachment.save()
                    content = part.get_payload(decode=True)  
                    attachment.file.save(str(fileName), ContentFile(content))
                    attachment.save()

    return "email synchronized"



@shared_task(name = "check_mails")
def check_mails():

    return "completed doing tasks"



