import json
import socket
from threading import Thread

from loguru import logger

from tools.frozen import get_path

logger.add(get_path('logs/server.log'))


class Server:

    def __init__(self, ip, port):
        self.connections = []  # 所有客户端连接
        logger.info('服务器启动中，请稍候...')
        self.state = False
        try:
            self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 监听者，用于接收新的socket连接
            self.listener.bind((ip, port))  # 绑定ip、端口
            self.listener.listen(5)  # 最大等待数
            self.state = True
        except OSError:
            logger.error('服务器启动失败，请检查ip端口是否被占用')
            exit()
        if self.state:
            logger.info('服务器启动成功：{}:{}'.format(ip, port))
        while True:
            client, _ = self.listener.accept()  # 阻塞，等待客户端连接
            user = Player(client, self.connections)
            self.connections.append(user)
            logger.info('新连接进入，IP:{}'.format(client.getpeername()[0]))
            logger.info('有新连接进入，当前连接数：{}'.format(len(self.connections)))


class Player:

    def __init__(self, client, connections):
        self.socket = client
        self.connections = connections
        self.name = None
        self.order = None
        self.login_state = False  # 登录状态
        self.data_handler()
        self.protocol_handler = ProtocolHandler()  # 协议处理对象

    def data_handler(self):
        # 给每个连接创建一个独立的线程进行管理
        thread = Thread(target=self.recv_data)
        thread.setDaemon(True)
        thread.start()

    def recv_data(self):
        # 接收数据
        try:
            while True:
                data = self.socket.recv(4096)  # 我们这里只做一个简单的服务端框架，只做粘包不做分包处理。
                if len(data) == 0:  # 数据为空则判断为玩家离线
                    logger.info('有玩家离线')
                    self.socket.close()
                    self.connections.remove(self)
                    break
                self.deal_data(data)  # 处理数据
        except ConnectionError:
            self.socket.close()
            self.connections.remove(self)
            logger.info('有用户发送的数据异常：' + bytes.decode() + '\n' + '已强制下线，详细原因请查看日志文件')

    def deal_data(self, data):
        """
        我们规定协议类型：
            1.每个数据包都以json字符串格式传输
            2.json中必须要有protocol字段，该字段表示协议名称
            登录协议：
                客户端发送：{"protocol":"login","username":"玩家账号"}
                服务端返回：{"protocol":"login","result":true,"order":‘’}
        """
        # 将字节流转成字符串再转为json数据
        protocol = eval(data.decode())
        # 根据协议中的protocol字段，直接调用相应的函数处理
        self.protocol_handler(self, protocol)

    def send(self, py_obj):
        """
        给玩家发送协议包
        py_obj:python的字典或者list
        """
        self.socket.sendall((json.dumps(py_obj, ensure_ascii=False) + '#').encode())

    def send_all_player(self, py_obj):
        """
        把这个数据包发送给所有在线玩家，包括自己
        """
        for player in self.connections:
            if player.login_state:
                player.send(py_obj)

    def send_without_self(self, py_obj):
        """
        发送给除了自己的所有在线玩家
        """
        for player in self.connections:
            if player is not self and player.login_state:
                player.send(py_obj)


class ProtocolHandler:
    """
    处理客户端返回过来的数据协议
    """

    def __call__(self, player, protocol):
        protocol_name = protocol['protocol']
        if not hasattr(self, protocol_name):
            player.send_without_self(protocol)
            return
        # 调用与协议同名的方法
        method = getattr(self, protocol_name)
        result = method(player, protocol)
        return result

    @staticmethod
    def login(player, protocol):
        player.login_state = True
        # 由于我们还没接入数据库，玩家的信息还无法持久化，所以我们写死几个账号在这里吧
        player.order = len(player.connections) - 1
        player.name = protocol['name']
        # 发送登录成功协议
        player.send({"protocol": "login", "login_state": True, "order": player.order})
        logger.info('玩家{}登录成功，order: {}，当前玩家数量: {}'.format(player.name, player.order, len(player.connections)))
        for i in player.connections:
            if i is not player and i.login_state:
                player.send({"protocol": "login", "opponent": i.name, 'order': i.order})
                i.send({"protocol": "login", "opponent": protocol['name'], 'order': player.order})
        if player.order == int(protocol['player_num']) - 1:
            player.send_all_player({"protocol": "login", "begin": True})
            logger.info('游戏开始')


if __name__ == '__main__':
    server = Server('0.0.0.0', 6666)
