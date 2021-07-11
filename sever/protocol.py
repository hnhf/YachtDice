from sever.room import Room
from loguru import logger


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
        server = player.server
        player.login_state = True
        # 由于我们还没接入数据库，玩家的信息还无法持久化，所以我们写死几个账号在这里吧
        player.order = len(player.connections) - 1
        player.name = protocol['name']
        room_num = protocol['room_num']
        if room_num not in [room.num for room in server.rooms]:
            new_room = Room(room_num)
            location = new_room.add_player(player)
            if location:
                server.rooms.append(new_room)
                player.room = new_room
                player.location = location
                logger.info("创建房间{}成功".format(room_num))
            else:
                logger.info("创建房间{}失败".format(room_num))
                return False
        else:
            logger.info("房间号已存在,加入中")
            current_room = [room for room in server.rooms if room.num == room_num][0]
            location = current_room.add_player(player)
            if location:
                player.location = location
                logger.info("加入房间{}成功".format(room_num))
            else:
                logger.info("加入房间{}失败".format(room_num))
                return False
        # 发送登录成功协议
        player.send({"protocol": "login", "order": player.order, 'login_state': True, 'room_num': room_num,
                     "location": player.location})

        # for i in player.connections:
        #     if i is not player and i.login_state:
        #         i.send({"protocol": "login", "opponent": protocol['name']})
        # if player.order == 1:
        #     player.send({"protocol": "login", "opponent": player.connections[0].name})
