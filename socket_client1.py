import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('192.168.31.8', 6666))
while True:
    for i in range(42):
        data = s.recv(1024)
        print(data)
        if int.from_bytes(data, byteorder='big', signed=False) == 41:
            break
        s.send(i.to_bytes(length=2, byteorder='big', signed=False))
        print('send', i, 'success')
        time.sleep(0.1)