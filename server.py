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
    print("Correct usage: script <IP address> <port number>")
    exit()

ipAddress = str(sys.argv[1])
port = int(sys.argv[2])

server.bind((ipAddress, port))
server.listen(7)

listOfClients = []
listOfMailsToBeSent = []
logData = []

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

def logThread(logData):
    while True:
        log = open("log.txt", "a")
        for data in logData:
            log.write(data)
            logData.remove(data)
        log.close()

def clientThread(connection, address):
    connection.send("Welcome!\n".encode('utf-8'))
    inputData = False
    data = ""
    mail = Mail()
    while True:
            if mail.isReady():
                listOfMailsToBeSent.append(mail)
                file = open("mail.txt", "a")
                file.write("FROM:" + mail.getFrom() + "\n")
                for rcpt in mail.getTo():
                    file.write("TO: " + rcpt + "\n")
                file.write("Data\n")
                file.write(mail.getData() + "\n")
                file.close()
                printMails(listOfMailsToBeSent)
                mail = Mail()
            try:
                message = connection.recv(2048).decode('utf8')
                if message:
                    message = message[:-1]
                    print("<" + address[0] + " " + str(address[1]) + "> " + message)
                    logData.append("<" + address[0] + " " + str(address[1]) + "> " + message + "\n")
                    if inputData:
                        if message != ".":
                            data+=(message + "\n")
                        else:
                            mail.setData(data)
                            response = "250 Ok: queued as 12345\n"
                            logData.append(response)
                            connection.send("250 Ok: queued as 12345\n".encode('utf8'))
                            inputData = False
                    elif "HELO:" in message.upper():
                        message = message.split()
                        message = message[1]
                        response = "250 " + str(message) + ", I am glad to meet you\n"
                        logData.append(response)
                        connection.send(response.encode('utf8'))
                    elif "MAIL FROM:" in message.upper():
                        message = message.split(' ')
                        message.pop(0)
                        message.pop(0)
                        mail.setFrom(message[0])
                        response = "250 ok\n"
                        logData.append(response)
                        connection.send(response.encode('utf8'))
                    elif "RCPT TO:" in message.upper():
                        message = message.split(' ')
                        message.pop(0)
                        message.pop(0)
                        mail.setTo(message[0])
                        response = "250 ok\n"
                        logData.append(response)
                        connection.send(response.encode('utf8'))
                    elif "DATA" in message.upper():
                        inputData = True
                        response = "354 End data with <CR><LF>.<CR><LF>\n"
                        logData.append(response)
                        connection.send(response.encode('utf8'))
                    elif "QUIT" in message.upper():
                        remove(connection)
                        response = "221 Bye\n"
                        logData.append(response)
                        logData.append("<" + address[0] + " " + str(address[1]) + "> has quit\n")
                        connection.send(response.encode('utf8'))
                        connection.close()
            except:
                continue

_thread.start_new_thread(logThread, (logData,))
while True:

    connection, address = server.accept()
    logData.append("<" + address[0] + " " + str(address[1]) + "> has connected\n")
    listOfClients.append(connection)
    print(address[0] + " connected")
    _thread.start_new_thread(clientThread, (connection, address))

conn.close()
server.close()
