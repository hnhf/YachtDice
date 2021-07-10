import json
import socket
from threading import Thread
from loguru import logger


class Server:
    """
    服务端主类
    """
    __user_cls = None

    def __init__(self, ip, port):
        self.connections = []  # 所有客户端连接
        logger.info('服务器启动中，请稍候...')
        try:
            self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 监听者，用于接收新的socket连接
            self.listener.bind((ip, port))  # 绑定ip、端口
            self.listener.listen(5)  # 最大等待数
        except:
            logger.info('服务器启动失败，请检查ip端口是否被占用。详细原因请查看日志文件')

        if self.__user_cls is None:
            logger.info('服务器启动失败，未注册用户自定义类')
            return

        logger.info('服务器启动成功：{}:{}'.format(ip, port))
        while True:
            client, _ = self.listener.accept()  # 阻塞，等待客户端连接
            user = self.__user_cls(client, self.connections)
            self.connections.append(user)

            logger.info('有新连接进入，当前连接数：{}'.format(len(self.connections)))

    @classmethod
    def register_cls(cls, sub_cls):
        """
        注册玩家的自定义类
        """
        if not issubclass(sub_cls, Connection):
            logger.info('注册用户自定义类失败，类型不匹配')
            return
        cls.__user_cls = sub_cls


class Connection:
    """
    连接类，每个socket连接都是一个connection
    """

    def __init__(self, client, connections):
        self.socket = client
        self.name = None
        self.connections = connections
        self.data_handler()

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
                if len(data) == 0:
                    logger.info('有玩家离线')
                    self.socket.close()
                    # 删除连接
                    self.connections.remove(self)
                    break
                # 处理数据
                self.deal_data(data)
        except:
            # self.socket.close()
            self.connections.remove(self)
            logger.error('{}玩家发送的数据异常：{},已强制下线'.format(self.name, data.decode()))

    def deal_data(self, data):
        """
        处理客户端的数据，需要子类实现
        """
        raise NotImplementedError


@Server.register_cls
class Player(Connection):

    def __init__(self, *args):
        self.login_state = False  # 登录状态
        self.order = None  # 玩家游戏中的相关数据
        self.protocol_handler = ProtocolHandler()  # 协议处理对象
        super().__init__(*args)

    def deal_data(self, data):
        """
        我们规定协议类型：
            1.每个数据包都以json字符串格式传输
            2.json中必须要有protocol字段，该字段表示协议名称
            登录协议：
                客户端发送：{"protocol":"login","username":"玩家账号"}
                服务端返回：{"protocol":"login","result":true,"order":‘’}
        """
        # 将字节流转成字符串
        event_str = data.decode()
        # 处理每一个协议,最后一个是空字符串，不用处理它
        protocol = eval(event_str)
        # 根据协议中的protocol字段，直接调用相应的函数处理
        self.protocol_handler(self, protocol)

    def send(self, py_obj):
        """
        给玩家发送协议包
        py_obj:python的字典或者list
        """
        self.socket.sendall((json.dumps(py_obj, ensure_ascii=False)).encode())

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
        py_obj['from'] = 'opponent'
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
        player.order = len(player.connections) - 1
        player.name = protocol['name']
        # 发送登录成功协议
        player.send({"protocol": "login", "order": player.order})
        for i in player.connections:
            if i is not player:
                i.send({"protocol": "login", "opponent": protocol['name']})
        if player.order == 1:
            player.send({"protocol": "login", "opponent": player.connections[0].name})


if __name__ == '__main__':
    server = Server('192.168.3.4', 6666)
