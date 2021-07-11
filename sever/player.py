import json
from threading import Thread

from loguru import logger

from sever.protocol import ProtocolHandler


class Connection:
    """
    连接类，每个socket连接都是一个connection
    """

    def __init__(self, server, client, connections):
        self.server = server
        self.socket = client
        self.name = None
        self.room = None
        self.room_num = None
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
        except ConnectionResetError:
            # self.socket.close()
            self.connections.remove(self)
            self.room.remove_player(self)
            logger.warning('{}玩家数据异常,退出房间：{}'.format(self.name, self.room.num))

    def deal_data(self, data):
        """
        处理客户端的数据，需要子类实现
        """
        raise NotImplementedError


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
