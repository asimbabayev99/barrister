import imaplib
import getpass
import email
import io  
import email.message


imap = imaplib.IMAP4_SSL('imap.yandex.ru')
login = imap.login('support@lua.az','support123')
imap_list = imap.list()
s
print(login)
print(imap_list)

print(imap.select('INBOX'))
print(imap.search(None, 'ALL'))
print(imap.fetch(b'1', '(RFC822)'))

print("-"*50)
status, data = imap.fetch(b'1', '(RFC822)')
msg = email.message_from_bytes(data[0][1], _class = email.message.EmailMessage)

print('subject', msg['Subject'])
print('mailing list',  msg['X-Mailing-List'])
print('date', msg['Date'])

payload = msg.get_payload()[ 0 ]
print(payload['Content-Type'])
payload.get_payload()