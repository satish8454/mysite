# Python Chat Application

This project is real-time chat application which built using django and daphne for socket communication.

## Prerequisites

In order to run the python script, your system must have the following programs/packages installed and the contact number should be saved in your phone (You can use bulk contact number saving procedure of email). There is a way without saving the contact number but has the limitation to send the attachment.
* Python 3.x

## Approach

### step 1
```
```

## Server Code
```
# Program to accept client request
# Author @inforkgodara

import socket

s = socket.socket()
host = socket.gethostname()
print(' Server will start on host : ', host)
port = 8080
s.bind((host, port))
print()
print('Waiting for connection')
print()
s.listen(1)
conn, addr = s.accept()
print(addr, ' Has connected to the server')
print()
while 1:
    message = input(str('>> '))
    message = message.encode()
    conn.send(message)
    print('Sent')
    print()
    incoming_message = conn.recv(1024)
    incoming_message = incoming_message.decode()
    print(' Client : ', incoming_message)
    print()
```
## Client Code
```
# Program to send request to the server
# Author @inforkgodara

import socket

s = socket.socket()
host = input(str('Enter hostname or host IP : '))
port = 8080
s.connect((host, port))
print('Connected to chat server')
while 1:
    incoming_message = s.recv(1024)
    incoming_message = incoming_message.decode()
    print(' Server : ', incoming_message)
    print()
    message = input(str('>> '))
    message = message.encode()
    s.send(message)
    print('Sent')
    print()
```
