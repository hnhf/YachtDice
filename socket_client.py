import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 建立连接:
s.connect(('112.232.240.231', 6666))
# 接收欢迎消息:
# print(s.recv(1024).decode('utf-8'))
s.send("你好呀，我是客户端".encode('utf8'))
input("")
# s.send(b'exit')
# s.close()
