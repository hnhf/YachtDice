import socket
from time import sleep

from loguru import logger
from threading import Thread
from sever.player import Connection, Player


class Server:
    """
    服务端主类
    """
    __user_cls = None

    def __init__(self, ip, port):
        self.connections = []  # 所有客户端连接
        self.rooms = []
        logger.info('服务器启动中，请稍候...')
        self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 监听者，用于接收新的socket连接
        self.listener.bind((ip, port))  # 绑定ip、端口
        self.listener.listen(5)  # 最大等待数

        logger.info('服务器启动成功：{}:{}'.format(ip, port))

    def run(self):
        while True:
            client, _ = self.listener.accept()  # 阻塞，等待客户端连接
            user = Player(self, client, self.connections)
            self.connections.append(user)
            c = self.connections[-1]
            logger.debug('connection 初始化 {}'.format(c.name))
            logger.info('新连接进入，IP:{}'.format(client.getpeername()[0]))
            logger.info('当前玩家数{}'.format(len(self.connections)))

    def clean_room(self):
        while True:
            for room in self.rooms:
                if len(room.players) == 0:
                    self.rooms.remove(room)
                    logger.debug("删除空闲房间{}".format(room.num))

    def info(self):
        while True:
            sleep(60)
            logger.info("玩家列表:{}".format([conn.name for conn in self.connections]))
            logger.info("房间列表:{}".format([room.num for room in self.rooms]))


def main():
    server = Server('192.168.3.4', 6666)
    threads = list()
    threads.append(Thread(target=server.run))
    threads.append(Thread(target=server.clean_room))
    threads.append(Thread(target=server.info))
    for thread in threads:
        thread.start()


if __name__ == '__main__':
    main()
