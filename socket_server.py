import socket
import threading

HOST = '192.168.31.8'
PORT = 6666
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(2)
information0 = []
information1 = []
players = [100, 200]
print('Waiting for connection...')


def tcp_link(sock, addr, i):
    print('Accept new connection from %s:%s...' % addr)
    sock.send(players[i].to_bytes(length=3, byteorder='big', signed=False))
    if i == 0:
        while True:
            data = sock.recv(1024)
            information0.append(data)
            if not data or int.from_bytes(data, byteorder='big', signed=False) == 41:
                break
            if len(information1) != 0:
                sock.send(information1[0])
                del(information1[0])
    elif i == 1:
        while True:
            data = sock.recv(1024)
            information1.append(data)
            if not data or int.from_bytes(data, byteorder='big', signed=False) == 41:
                break
            if len(information0) != 0:
                sock.send(information0[0])
                del(information0[0])
    sock.close()
    print('Connection from %s:%s closed.' % addr)


while True:
    for i in range(2):
        sock, addr = s.accept()
        t = threading.Thread(target=tcp_link, args=(sock, addr, i))
        t.start()
