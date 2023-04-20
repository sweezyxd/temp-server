import socket
import time
from threading import Thread

server = socket.socket()
host = '127.0.0.1'
port = 8080
try:
    server.bind((host, port))
except socket.error as e:
    print(str(e))
print('Server is listening...')
server.listen(5)
userarr, namearr = [], []


class Clnt:
    def __init__(self, client, name, obj):
        self.rcv = None
        self.obj = obj
        self.data = None
        self.on = True
        self.client = client
        self.name = name
        self.main()

    def main(self):
        if self.on:
            self.rcv = Thread(target=self.receive)
            self.rcv.start()

    def send(self, text):
        try:
            self.client.send(text)
        except ConnectionResetError:
            sendtoall(self.end())

    def end(self):
        namearr.remove(self.name)
        userarr.remove(globals()[self.obj])
        self.on = False
        del globals()[self.obj]
        temp = ""
        for name in namearr:
            temp += " " + name
        print(temp)
        sendtoall(("<start_name_arr>" + temp + "<end_name_arr>").encode())
        return (str(self.name) + " has disconnected.\n").encode()

    def receive(self):
        try:
            while self.on:
                data = self.client.recv(1024)
                if len(data.decode()) - len(self.name) - 2 <= 0:
                    data = self.end()
                sendtoall(data)
        except ConnectionResetError:
            sendtoall(self.end())
            temp = ""
            for name in namearr:
                temp += " " + name
            print(temp)
            sendtoall(("<start_name_arr>" + temp + "<end_name_arr>").encode())


def main():
    users = 0
    while True:
        Client, address = server.accept()
        users += 1
        time.sleep(1)
        username = Client.recv(128)
        if username.decode() in namearr:
            Client.send(b"<>username_taken<!>")
            Client.close()
        elif " " in username.decode():
            Client.send(b"<>username_format_incorrect<!>")
            Client.close()
        else:
            globals()["Clnt" + str(users)] = Clnt(Client, username.decode(), "Clnt" + str(users))
            userarr.append(globals()["Clnt" + str(users)])
            namearr.append(username.decode())
            sendtoall((username.decode() + " has connected.\n").encode())
            temp = ""
            for name in namearr:
                temp += " " + name
            print(temp)
            sendtoall(("<start_name_arr>" + temp + "<end_name_arr>").encode())
            time.sleep(1)


def sendtoall(s):
    for user in userarr:
        user.send(s)


start = Thread(target=main)
if __name__ == '__main__':
    main()
