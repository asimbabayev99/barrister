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
def synchronize_mail():
  for email in EmailAccount.objects.all():


    print("start to synchronize mail")
    server = 'imap.yandex.ru'
    mail = imaplib.IMAP4_SSL(server)
    try:
      mail.authenticate('XOAUTH2',lambda x: GenerateOAuth2String(email.email,email.token,base64_encode=False))
    except:
      continue
    mail_folders = ['Inbox','Drafts','Sent','Trash']
    user = EmailAccount.objects.get(email=email.email).user

    # loop th rough mail folders
    for folder in mail_folders:
        mail.select("{0}".format(folder))
        type, data = mail.search(None, 'ALL')
        try:
          database_emails = frozenset(list(Email.objects.filter(folder=folder).values_list('num')))
          actual_emails = frozenset(data[0].split())
          print(actual_emails.difference(database_emails))

          last_num = Email.objects.filter(folder=folder).order_by('-date')[0].num
        except:
          last_num = 0
        for num in data[0].split()[::-1]:
            
            num = num.decode()
            print(num,last_num)
            if num == last_num:
              break
            typ, data = mail.fetch(num, '(RFC822)' )
            raw_email = data[0][1]
            # converts byte literal to string removing b''
          
            email_message = mailparser.parse_from_bytes(raw_email)
            subject = email_message.subject
            sender = email_message.from_[0][1]
            receiver = email_message.to[0][1]
            date = email_message.date
            # timestamp = email.utils.parsedate_tz(date)

            new_email, created = Email.objects.get_or_create(folder=folder,user=user,num=num, sender=sender, receiver=receiver, date=date)
            print('num:',num,'last_num:',last_num)
            if created:
              continue
            # print("folder=", folder, "num=", num, "sender=", sender, "receiver=", receiver, "date=", date)
            # if  not created:
            #     print("already created")
            #     continue
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



@shared_task(name = "get_last_mail")
def get_last_mails(email,token):


  print("getting last mails")
  server = 'imap.yandex.ru'
  mail = imaplib.IMAP4_SSL(server)
  try:
    mail.authenticate('XOAUTH2',lambda x: GenerateOAuth2String(email,token,base64_encode=False))
  except:
    print('CANT CONNECT IMAP SERVER')
  mail_folders = ['Inbox','Drafts','Sent','Trash']
  user = EmailAccount.objects.get(email=email).user

  # loop th rough mail folders
  for folder in mail_folders:
      mail.select("{0}".format(folder))
      type, data = mail.search(None, 'ALL')
      try:
        last_num = Email.objects.filter(folder=folder).order_by('-date')[0].num
      except:
          last_num = 0
      for num in data[0].split()[::-1]:
        num = num.decode()
        if num == last_num:
          break
        typ, data = mail.fetch(num, '(RFC822)' )
        raw_email = data[0][1]
        # converts byte literal to string removing b''
          
        email_message = mailparser.parse_from_bytes(raw_email)
        subject = email_message.subject
        sender = email_message.from_[0][1]
        receiver = email_message.to[0][1]
        date = email_message.date
        # timestamp = email.utils.parsedate_tz(date)

        new_email, created = Email.objects.get_or_create(folder=folder,user=user,num=num, sender=sender, receiver=receiver, date=date)
        if created:
          continue
        print('num:',num,'last_num:',last_num)
            
        # print("folder=", folder, "num=", num, "sender=", sender, "receiver=", receiver, "date=", date)
        # if  not created:
        #     print("already created")
        #     continue
        new_email.subject = subject
        content = email_message.text_html[0] if email_message.text_html != [] else ""
        new_email.content = content
        new_email.save()
        if email_message.attachments is not None:
          for i in email_message.attachments:

            attachment = Attachment(name=i['filename'],email=new_email)
            attachment.file.save(i['filename'],ContentFile(base64.b64decode(i['payload'])))
            attachment.save()

  
  return "completed doing tasks"



@shared_task(name = "check_mails")
def check_mails():
  server = 'imap.yandex.ru'
  mail = imaplib.IMAP4_SSL(server)
  try:
    mail.authenticate('XOAUTH2',lambda x: GenerateOAuth2String(email,token,base64_encode=False))
  except:
    print('CANT CONNECT IMAP SERVER')
  num_list = Email.objects.values_list('num')
  mail_folders = ['Inbox','Drafts','Sent','Trash']
  for folder in mail_folders:
    mail.select("{0}".format(folder))
    type,data = mail.search(None,'ALL')
    for num in num_list:
      if num not in set(data[0].split()):
        Email.objects.get(num=num).delete()
      else:
        continue









   
   




