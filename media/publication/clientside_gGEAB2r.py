import socket
import sys 
import time

s =  socket.socket()
host = socket.gethostname()
port = 80
s.connect((host,port))
print('client connected succesfully')

while True:
    incoming_message = s.recv(1024)
    incoming_message = incoming_message.decode()
    print('Server:{0}'.format(incoming_message))
    message = input(str('>>'))
    s.send(message.encode())
    print('Message has been sent')

