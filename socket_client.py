import socket

s = socket.socket()
s.connect(('112.232.240.231', 6666))
s.send("你好呀，我是客户端".encode('utf8'))
input("")