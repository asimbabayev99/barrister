from __future__ import absolute_import, unicode_literals
from celery import shared_task
from datetime import timezone, datetime
import  time
from django.core.files.base import ContentFile
import imaplib
import imapclient
import base64
import os
import email
import mailparser
from dateutil import parser
# models
from account.models import CustomUser
from home.models import EmailAccount, Email, Attachment , Receiver




  

  
@shared_task(name='delete_mail')
def delete_mail(folders):
  client = imapclient.IMAPClient('imap.yandex.ru')
  client.oauth2_login('azadmammedov@yandex.ru','AgAAAAA9U6WoAAZmeTTDasOXdE9usp_-zAmOL_E')
  for folder,uids in folders.items():
    print(uids)
    client.select_folder(folder)
    print(client.delete_messages(uids))
  return "Mails deleted"











@shared_task(name = "synchronize_mail")
def synchronize_mail():
  for email in EmailAccount.objects.all():
    print("start to synchronize mail")
    server = 'imap.yandex.ru'
    mail = imapclient.IMAPClient('imap.yandex.ru')
    try:
      mail.oauth2_login(email.email,email.token)
    except:
      continue
    mail_folders = ['Inbox','Drafts','Sent','Spam']
    user = EmailAccount.objects.get(email=email.email).user
    # loop th rough mail folders
    for folder in mail_folders:
      mail.select_folder(folder)
      messages = mail.search('All')
      #remove deleted emails from database
      try:
        last_num = Email.objects.filter(folder=folder).last().num
      except:
        last_num = 0 
      print(last_num) 
      db_uids = set([int(x[0]) for x in Email.objects.filter(folder=folder).order_by('num').values_list('num')])
      actual_uids = set(mail.fetch(messages,'RFC822').keys())
      print('-'*30)
      print('folder:',folder)
      print('db:',db_uids)
      print('actual:',actual_uids)
      print('difference:',db_uids.difference(actual_uids))
      for i in db_uids.difference(actual_uids):
        Email.objects.filter(folder=folder,num=i).delete()
      print('-'*30)
      # messages = mail.search('UNSEEN')
      print(messages)
      for uid, message_data in mail.fetch(messages,'RFC822').items():
        if int(last_num) < uid:

          mail.add_flags(uid,'\Seen')
          raw_email = message_data['RFC822'.encode()]
          # converts byte literal to string removing b''
          email_message = mailparser.parse_from_bytes(raw_email)
          created = False
          try:
            new_email = Email.objects.get(folder=folder,user=user,num=uid, sender=sender, receiver=receiver, date=date)
            created=True
          except:
            new_email = Email()
          if created:
            continue
          new_email.user = user
          new_email.num = uid
          new_email.sender = email_message.from_[0][1]
          new_email.date = email_message.date 
          
          new_email.subject = email_message.subject if email_message.subject != "" else 'No subject'
          content = email_message.text_html[0] if email_message.text_html != [] else ""
          new_email.content = content
          new_email.folder = folder
          new_email.flag = 'Unseen'
          new_email.save()
          for i in email_message.to:
            Receiver.objects.create(email=new_email,receiver=i[1])
          if email_message.attachments is not None:
            for i in email_message.attachments:
              print(i['filename'])
              if Attachment.objects.filter(name=i['filename'],email=new_email).exists():
                continue
              attachment = Attachment(name=i['filename'],email=new_email)
              attachment.file.save(i['filename'],ContentFile(base64.b64decode(i['payload'])))              
              attachment.save()
         


  return "email synchronized"



@shared_task(name = "get_last_mail")
def get_last_mails(email,token):
  account = EmailAccount.objects.get(email=email,token=token)
  client = imapclient.IMAPClient('imap.yandex.ru')
  client.oauth2_login(email,token)
  mail_folders = ['Inbox','Spam',]
  user = EmailAccount.objects.get(email=email).user
  # loop th rough mail folders
  for folder in mail_folders:
    client.select_folder(folder)
    messages = client.search(['UNSEEN','NOT','Flagged'])
    try:
      last_num = Email.objects.filter(folder=folder).last().num
    except:
      last_num = 0 
    for uid, message_data in client.fetch(messages,'RFC822').items():
      if int(last_num) < uid:   
        raw_email = message_data['RFC822'.encode()]
        email_message = mailparser.parse_from_bytes(raw_email)
        created = False
        try:
          new_email = Email.objects.get(folder=folder,user=user,num=uid, sender=sender, receiver=receiver, date=date)
          created=True
        except:
          new_email = Email()
        if created:
          continue
        new_email.user = user
        new_email.num = uid
        new_email.sender = email_message.from_[0][1]
        new_email.date = email_message.date 
        
        new_email.subject = email_message.subject if email_message.subject != "" else 'No subject'
        content = email_message.text_html[0] if email_message.text_html != [] else ""
        new_email.content = content
        new_email.folder = folder
        new_email.flag = 'Unseen'
        new_email.save()
        for i in email_message.to:
          Receiver.objects.create(email=new_email,receiver=i[1])
        if email_message.attachments is not None:
          for i in email_message.attachments:
            print(i['filename'])
            if Attachment.objects.filter(name=i['filename'],email=new_email).exists():
              continue
            attachment = Attachment(name=i['filename'],email=new_email)
            attachment.file.save(i['filename'],ContentFile(base64.b64decode(i['payload'])))              
            attachment.save()
   
  
  return 'Last mails saved'
  

  

  
  
  
    
  















   
   




