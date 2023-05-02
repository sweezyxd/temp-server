import socket as s
from threading import Thread

server = s.socket()
host = 'localhost'
port = 6969

try:
    server.bind((host, port))
except s.error as e:
    print(str(e))
print('Server is listening...')
server.listen(5)
client, address = server.accept()
print("Connected...")


class Shell:
    def __init__(self):
        self.on = True
        self.start()

    def snd(self):
        while self.on:
            txt = input()
            client.send(txt.encode())
            if txt == "exit":
                self.on = False

    def start(self):
        Thread(target=self.snd).start()
        while self.on:
            print(client.recv(1024).decode(), end="")


Shell()
