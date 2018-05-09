import socket
import sys
import _thread

class Mail:
    def __init__(self):
        self.data = ""
        self.fromUser = ""
        self.to = []
    def getData(self):
        return self.data
    def getFrom(self):
        return self.fromUser
    def getTo(self):
        return self.to
    def setData(self, data):
        self.data = data
    def setFrom(self, fromUser):
        self.fromUser = fromUser
    def setTo(self, to):
        self.to.append(to)
    def isReady(self):
        if len(self.data) >= 1 and len(self.fromUser) >= 1 and len(self.to) >= 1:
            return True
        else:
            return False

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

if len(sys.argv) != 3:
    print("Correct usage: script, IP address, port number")
    exit()

ipAddress = str(sys.argv[1])
port = int(sys.argv[2])

server.bind((ipAddress, port))
server.listen(7)

listOfClients = []
listOfMailsToBeSent = []

def remove(connection):
    if connection in listOfClients:
        listOfClients.remove(connection)

def broadcast(message, connection):
    for client in listOfClients:
        if client != connection:
            try:
                client.send(message)
            except:
                continue

def printMails(listOfMailsToBeSent):
    for mail in listOfMailsToBeSent:
        print("FROM: ", mail.getFrom())
        for rcpt in mail.getTo():
            print("RCPT TO: ", rcpt)
        print("DATA ", mail.getData()[:-1])

def clientThread(connection, address):
    connection.send("Welcome!\n".encode('utf-8'))
    inputData = False
    data = ""
    mail = Mail()
    while True:
            if mail.isReady():
                listOfMailsToBeSent.append(mail)
                printMails(listOfMailsToBeSent)
                mail = Mail()
            try:
                message = connection.recv(2048).decode('utf8')
                if message:
                    message = message[:-1]
                    print("<" + address[0] + " " + str(address[1]) + "> " + message)
                    if inputData:
                        if message != ".":
                            data+=(message + "\n")
                        if message == ".":
                            mail.setData(data)
                            connection.send("250 Ok: queued as 12345\n".encode('utf8'))
                            inputData = False
                    elif "HELO:" in message.upper():
                        message = message.split()
                        message = message[1]
                        response = "250 " + str(message) + ", I am glad to meet you\n"
                        connection.send(response.encode('utf8'))
                    elif "MAIL FROM:" in message.upper():
                        message = message.split(' ')
                        message.pop(0)
                        message.pop(0)
                        mail.setFrom(message[0])
                        response = "250 ok\n"
                        connection.send(response.encode('utf8'))
                    elif "RCPT TO:" in message.upper():
                        message = message.split(' ')
                        message.pop(0)
                        message.pop(0)
                        mail.setTo(message[0])
                        response = "250 ok\n"
                        connection.send(response.encode('utf8'))
                    elif "DATA" in message.upper():
                        inputData = True
                        connection.send("354 End data with <CR><LF>.<CR><LF>\n".encode('utf8'))
                    elif "QUIT" in message.upper():
                        remove(connection)
                        connection.send("21 Bye\n".encode('utf8'))
                        connection.close()
                    # broadcast(messageToSend.encode('utf-8'), connection)
            except:
                continue

while True:

    connection, address = server.accept()
    listOfClients.append(connection)
    print(address[0] + " connected")
    _thread.start_new_thread(clientThread,(connection, address))

conn.close()
server.close()
