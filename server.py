import socket
import sys
import _thread

class Message:
    def __init__(self):
        self.data = ""
        self.fromUser = ""
        self.to = ""
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
        self.to = to
    def isReady(self):
        if len(self.data) > 1 and len(self.fromUser) > 1 and len(self.to) > 1:
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

def broadcast(message, connection):
    for client in listOfClients:
        if client != connection:
            try:
                client.send(message)
            except:
                continue

def clientThread(connection, address):
    connection.send("Welcome!\n".encode('utf-8'))
    while True:
            try:
                message = connection.recv(2048).decode('utf8')
                if message:
                    print("<" + address[0] + " " + address[1] + "> " + message[:-1])
                    messageToSend = "<" + address[0] + "> " + message
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
