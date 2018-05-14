import socket
import sys
import syslog
import _thread
import time

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

syslog.openlog(logoption=syslog.LOG_PID, facility=syslog.LOG_MAIL)
listOfClients = []
listOfMailsToBeSent = []
logData = []
rubyData = []
userList = []

ips = open('./ips.txt', 'r')
lines = ips.readlines()
userList = []

for i in lines:
    data = i[:-1].split()
    userList.append((data[0], data[1], data[2]))
ips.close()

def relay(mail):
    for rcpt in mail.getTo():
        if "MAURICIO" in rcpt.upper():
            pass
        else:
            index = getIndexOfUser(rcpt)
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                host = userList[index][1]
                port = int(userList[index][2])
                s.connect((host, port))
                s.send("helo: mauricio\n".encode('utf8'))
                time.sleep(1)
                mailFrom = "from: " + str(mail.getFrom()) + "\n"
                mailTo = "rcpt to: " + str(userList[index][0]) + "\n"
                logData.append("sending: " + str(mailFrom))
                logData.append("sending: " + str(mailTo))
                logData.append("sending: " + str(mail.getData()))
                s.send(mailFrom.encode('utf8'))
                time.sleep(1)
                s.send(mailTo.encode('utf8'))
                time.sleep(1)
                s.send("data\n".encode('utf8'))
                time.sleep(1)
                s.send(mail.getData().encode('utf8'))
                time.sleep(1)
                s.send(".\n".encode('utf8'))
                s.send("quit\n".encode('utf8'))
                time.sleep(1)
                s.close()
            except:
                logData.append("could not send mail to " + str(userList[index][0]))


def getIndexOfUser(userToCheck):
    for index, user in enumerate(userList):
        if user[0] == userToCheck:
            return index

def userInList(userToCheck):
    for user in userList:
        if user[0] == userToCheck:
            return True

def sendToRuby(user):
    rubyData = []
    mailbox = open('./mail.txt', 'r')
    mails = mailbox.readlines()
    mailToMe = 0
    hasMe = False
    startIndex = 0
    startOfHasMe = False
    finishIndex = 0
    finishOfHasMe = False
    userToCheckFor = "to: " + str(user)
    data = []
    for index, mail in enumerate(mails):
        if "FROM: " in mail.upper():
            startIndex = index
            startOfHasMe = True

        if userToCheckFor.upper() in mail.upper():
            mailToMe = index
            hasMe = True

        if "mailFinished" in mail and hasMe:
            finishIndex = index
            finishOfHasMe = True

        if finishOfHasMe and hasMe and startOfHasMe:
            finishOfHasMe = False
            hasMe = False
            startOfHasMe = False
            while startIndex < finishIndex:
                data.append(mails[startIndex])
                startIndex += 1
    return data
    mailbox.close()


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
            syslog.syslog("SMTP Server: "  + data)
            log.write(data)
            logData.remove(data)
        log.close()

def clientThread(connection, address):
    connection.send("Welcome!\n".encode('utf-8'))
    inputData = False
    ruby = False
    data = ""
    mail = Mail()
    sendingMail = mail
    while True:
            if mail.isReady():
                sendingMail = mail
                listOfMailsToBeSent.append(mail)
                file = open("mail.txt", "a")
                file.write("FROM: " + mail.getFrom() + "\n")
                for rcpt in mail.getTo():
                    file.write("TO: " + rcpt + "\n")
                file.write("Data\n")
                file.write(mail.getData() + "\n")
                file.write("mailFinished\n")
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
                            time.sleep(1)
                            connection.send(response.encode('utf8'))
                            inputData = False
                    elif ruby:
                        if userInList(message):
                            logData.append(message + "\n")
                            response = "user has an inbox\n"
                            connection.send(response.encode('utf8'))
                            logData.append(response)
                            data = sendToRuby(message)
                            for line in data:
                                connection.send(line.encode('utf8'))
                            response = "To view your mail again or view newest mail re-run the ruby script\n"
                            connection.send(response.encode('utf8'))
                            logData.append(response)
                            connection.close()
                    elif "HELO:" in message.upper():
                        message = message.split()
                        message = message[1]
                        response = "250 " + str(message) + ", I am glad to meet you\n"
                        logData.append(response)
                        time.sleep(1)
                        connection.send(response.encode('utf8'))
                    elif "MAIL FROM:" in message.upper():
                        message = message.split(' ')
                        message.pop(0)
                        message.pop(0)
                        mail.setFrom(message[0])
                        response = "250 ok\n"
                        logData.append(response)
                        time.sleep(1)
                        connection.send(response.encode('utf8'))
                    elif "RCPT TO:" in message.upper():
                        message = message.split(' ')
                        message.pop(0)
                        message.pop(0)
                        mail.setTo(message[0])
                        response = "250 ok\n"
                        logData.append(response)
                        time.sleep(1)
                        connection.send(response.encode('utf8'))
                    elif "DATA" in message.upper():
                        inputData = True
                        response = "354 End data with <CR><LF>.<CR><LF>\n"
                        logData.append(response)
                        time.sleep(1)
                        connection.send(response.encode('utf8'))
                    elif "QUIT" in message.upper():
                        remove(connection)
                        response = "221 Bye\n"
                        logData.append(response)
                        logData.append("<" + address[0] + " " + str(address[1]) + "> has quit\n")
                        time.sleep(1)
                        connection.send(response.encode('utf8'))
                        connection.close()
                        relay(sendingMail)
                        sendingMail = Mail()
                    elif "RUBY" in message.upper():
                        ruby = True
                    else:
                        badCommand = "errorBadCommand " + message + "\n"
                        logData.append(badCommand)
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
syslog.close()
