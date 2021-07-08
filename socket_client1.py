import socket
import time
import threading

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('192.168.31.8', 6666))


def tcp_send():
    for i in range(42):
        s.send(i.to_bytes(length=2, byteorder='big', signed=False))
        time.sleep(0.2)

def tcp_receive():
    pass


for i in range(42):
    s.send(i.to_bytes(length=2, byteorder='big', signed=False))
    print('send', i, 'success')
    time.sleep(0.1)
    data = s.recv(1024)
    print(data)
    if int.from_bytes(data, byteorder='big', signed=False) == 41:
        break
    s.send(i.to_bytes(length=2, byteorder='big', signed=False))
    print('send', i, 'success')
    time.sleep(0.1)

while True:
    send = threading.Thread(target=tcp_send)
    send.start()
    receive = threading.Thread(target=tcp_receive)
    receive.start()
