import socket
import sys
import traceback
from threading import Thread

import users
import messages

host = "0.0.0.0"
port = 3555
ips = open("ips.txt", "r")
lines = ips.readlines()
userList = []

for i in lines:
    data = i[:-1].split()
    userList.append(users.User(data[0], data[1]))

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))

server.listen(6)


mail = messages.Message()
while True:
   connection, address = server.accept()
   print("Got a connection from %s" % str(address))
   dataInput = False
   message = 'Thank you for connecting\n'
   connection.send(message.encode('utf8'))
   while True:
       data = connection.recv(1024).decode('utf8')[:-1]
       print(data)
       if mail.isReady():
           print(mail.getFrom())
           print(mail.getTo())
           print(mail.getData())
       if "HELO" in data.upper():
           data = data.split()
           data = data[1]
           mail.setFrom(data)
           message = "250 " + data + ", I am glad to meet you\n"
           connection.send(message.encode('utf8'))
       elif "MAIL FROM" in data.upper():
           data = data.split(' ')
           data.pop(0)
           data.pop(0)
           data = " ".join(str(x) for x in data)
           message = "250 ok\n"
           connection.send(message.encode('utf8'))
       elif "RCPT TO" in data.upper():
           data = data.split(' ')
           data.pop(0)
           data.pop(0)
           data = " ".join(str(x) for x in data)
           mail.setTo(data)
           message = "250 ok\n"
           connection.send(message.encode('utf8'))
       elif dataInput:
           mail.setData(data)
           message = "End data by pressing enter\n"
           connection.send(message.encode('utf8'))
           dataInput = False
       elif "DATA" in data.upper():
           dataInput = True
           message = "354 End data by pressing enter\n"
           connection.send(message.encode('utf8'))
       if data == "quit":
           connection.close()
           server.close()
