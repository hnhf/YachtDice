import socket
from loguru import logger

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


if __name__ == '__main__':
    server = Server('192.168.3.4', 6666)
    server.run()
