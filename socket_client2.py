import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('192.168.31.8', 6666))
s.setblocking(0)

while True:
    try:
        data = s.recv(1024)
        print(data)
    except:
        pass


