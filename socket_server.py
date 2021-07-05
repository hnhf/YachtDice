import socket
import threading

HOST = '192.168.31.8'
PORT = 6666
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(2)
information0 = []   # 记录第一位的消息
information1 = []   # 记录第二位的消息
players = [100, 200]    # 分别发送给两位的消息
print('Waiting for connection...')


def tcp_link(sock, addr, i):
    print('Accept new connection from %s:%s...' % addr)
    sock.send(players[i].to_bytes(length=3, byteorder='big', signed=False))
    if i == 0:                          # 如果这是第一位连接者
        while True:
            data = sock.recv(1024)      # 接收第一位连接者的消息
            information0.append(data)   # 并记录
            if not data or int.from_bytes(data, byteorder='big', signed=False) == 41:
                break
            if len(information1) != 0:  # 把第二位连接者的信息挨个发送过去
                sock.send(information1[0])
                del(information1[0])

    elif i == 1:                        # 如果这是第二位连接者
        while True:
            data = sock.recv(1024)      # 接收第一位连接者的消息
            information1.append(data)   # 并记录
            if not data or int.from_bytes(data, byteorder='big', signed=False) == 41:
                break
            if len(information0) != 0:  # 把第一位连接者的信息挨个发送过去
                sock.send(information0[0])
                del(information0[0])
    sock.close()
    print('Connection from %s:%s closed.' % addr)


while True:
    for i in range(2):
        sock, addr = s.accept()
        t = threading.Thread(target=tcp_link, args=(sock, addr, i))
        t.start()
