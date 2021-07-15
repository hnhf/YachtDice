# -*- coding: utf-8 -*-
"""
Created on Thu Jul  1 17:14:09 2021
@author: Fan
"""
import json
import random
import math
import sys
import numpy as np
import pygame
from pygame.locals import *
from loguru import logger
from conf import config
import socket
from tools.frozen import get_path
from threading import Thread

pygame.display.set_caption('游艇骰子')
pygame.init()
font_roll = pygame.font.Font(get_path('resource/font/simhei.ttf'), config.roll_font)
font_score = pygame.font.Font(get_path('resource/font/simhei.ttf'), 20)
font_player = pygame.font.Font(get_path('resource/font/simhei.ttf'), 28)
font_20 = pygame.font.Font(get_path('resource/font/simhei.ttf'), 20)
font_25 = pygame.font.Font(get_path('resource/font/simhei.ttf'), 25)
font_30 = pygame.font.Font(get_path('resource/font/simhei.ttf'), 30)
IP = '10.166.23.147'
PORT = 6666
# 建立socket连接
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP, PORT))


class Ytz(object):
    def __init__(self, name, number):
        #  self.play_music(get_path('resource/audio/caromhall.mp3'), 0.08, -1)
        self.screen = pygame.display.set_mode((config.x_length, config.y_length))
        self.bg_color = config.white
        self.bg_picture = pygame.image.load(get_path('resource/images/background.jpg'))
        self.img = [pygame.image.load(get_path('resource/images/0.jpg')),
                    pygame.image.load(get_path('resource/images/01.png')),
                    pygame.image.load(get_path('resource/images/02.png')),
                    pygame.image.load(get_path('resource/images/03.png')),
                    pygame.image.load(get_path('resource/images/04.png')),
                    pygame.image.load(get_path('resource/images/05.png')),
                    pygame.image.load(get_path('resource/images/06.png'))]
        self.player_num = int(number)
        self.name = name  # 玩家昵称
        self.order = 0  # 玩家顺序
        self.player = None  # 当前回合玩家
        self.login_state = False
        self.player_list = {self.name: self.order}
        self.game_turn = 1  # 回合数
        self.roll_time = 0  # 本回合摇骰子次数
        self.dice = [0, 0, 0, 0, 0]  # 当前骰子点数
        self.selected_dice = []  # 选择要摇的骰子
        self.score_now = np.zeros(17, dtype=int)  # 临时显示本次摇骰子的各项分数
        self.score_record = {self.name: {}}  # 已经记录的分数
        for i in range(17):  # 创建dict对象来记录两位玩家的分数，False表示未计分
            self.score_record[self.name].update(
                {i: {"score": 0, "recorded": False}})
        for j in [7, 15, 16]:  # 对于Bonus和总分项不需要点击登记，而是实时计算
            self.score_record[self.name][j]["recorded"] = True

    # 画出游戏界面
    def draw_board(self):

        # 显示出五个骰子和摇骰子按钮
        self.screen.fill(self.bg_color)
        self.screen.blit(self.bg_picture, (0, 100))
        for i in range(5):
            self.screen.blit(self.img[self.dice[i]], (i * config.dice_length + 10, 10))
        for k in self.selected_dice:
            pygame.draw.rect(self.screen, config.red, [k * 100 + 5, 5, 90, 90], 3)
        pygame.draw.circle(self.screen, config.gray, config.roll_circle_position, 2 * config.roll_font / 3)
        self.screen.blit(font_roll.render('摇', True, config.red), config.roll_position)

        # 显示出游戏玩家
        player_location = config.locations[self.player_num - 2]
        self.screen.blit(font_player.render('回合{}/13'.format(math.ceil(self.game_turn / 2)), True, config.black),
                         (42, 105))
        self.screen.blit(font_25.render('{}/3'.format(self.roll_time), True, config.black), (531, 75))
        player_color = [config.black, config.black, config.black]
        player_color[self.player_list[self.player]] = config.red

        # 显示出各项分数
        for player, order in self.player_list.items():
            self.screen.blit(font_player.render(player, True, player_color[order]),
                             (player_location[order] - 30, config.dice_length + 5))
            for key, value in self.score_record[player].items():
                if self.score_record[player][key]["recorded"]:
                    single_score = font_score.render(str(self.score_record[player][key]["score"]), True,
                                                     config.black)
                    self.screen.blit(single_score, (player_location[order], config.dice_length + config.list_y_length +
                                                    config.score_font / 2 + key * config.list_y_length))
                if player == self.player and not self.score_record[player][key]["recorded"]:
                    single_score = font_score.render(str(self.score_now[key]), True, config.gray)
                    self.screen.blit(single_score, (player_location[order], config.dice_length + config.list_y_length +
                                                    config.score_font / 2 + key * config.list_y_length))

        # 显示出屏幕左边的得分列表
        for j in range(17):
            if j == 7 or j == 15:
                score_list = font_25.render(config.score_list[j], True, config.black)
                self.screen.blit(score_list, (60, 6 + config.dice_length + (j + 1) * config.list_y_length))
            elif j == 16:
                score_list = font_30.render(config.score_list[j], True, config.black)
                self.screen.blit(score_list, (70, 4 + config.dice_length + (j + 1) * config.list_y_length))
            else:
                score_list = font_20.render(config.score_list[j], True, config.black)
                self.screen.blit(score_list, (80, 8 + config.dice_length + (j + 1) * config.list_y_length))

        # 用横线将各项分数分隔开
        for i in range(18):
            pygame.draw.line(self.screen, config.black, (0, config.dice_length + config.list_y_length * i),
                             (config.x_length, config.dice_length + config.list_y_length * i), 2)
        pygame.draw.line(self.screen, config.black, (config.list_x_length, config.dice_length),
                         (config.list_x_length, config.y_length),
                         3)

        # 根据玩家数量用竖线把各玩家分数隔开
        for i in range(self.player_num):
            pygame.draw.line(self.screen, config.black,
                             (config.list_x_length + i * config.list_player_length / self.player_num, config.dice_length),
                             (config.list_x_length + i * config.list_player_length / self.player_num, config.y_length), 3)
        pygame.display.update()

    # 弹出提示
    def draw_text(self, text, xx, yy, size):
        pygame.font.init()
        fontObj = pygame.font.Font(get_path('resource/font/simhei.ttf'), size)
        textSurfaceObj = fontObj.render(text, True, config.white, config.black)
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.center = (xx, yy)
        self.screen.blit(textSurfaceObj, textRectObj)
        pygame.display.update()

    # 检查事件，一个返回字典
    def check_event(self, event):
        if event.type == QUIT:
            return {"protocol": 'offline', "button": 'quit', 'from': self.name}
        if event.type == MOUSEBUTTONDOWN:  # 鼠标点击，根据点击位置返回数字
            (mouse_x, mouse_y) = pygame.mouse.get_pos()
            for i in range(5):
                if (mouse_x - (i * config.dice_length + config.dice_length / 2)) ** 2 + (
                        mouse_y - config.dice_length / 2) ** 2 < config.select_range ** 2:
                    return {"protocol": 'select_dice', "button": i, 'from': self.name}
            if (mouse_x - config.roll_circle_position[0]) ** 2 + (
                    mouse_y - config.roll_circle_position[1]) ** 2 < config.select_range ** 2:
                return {"protocol": "roll_dice", "button": "down", 'from': self.name}  # 鼠标在摇按钮处点下
            for i in range(17):  # 如果点击的位置是自己分数的位置的话
                if (mouse_x - config.locations[self.player_num][self.player_list[self.name]]) ** 2 + (
                        mouse_y - (config.dice_length + config.list_y_length * 1.5 + i * config.list_y_length)) ** 2 < (
                        config.list_y_length / 2) ** 2:
                    return {"protocol": "record_score", "button": i, 'from': self.name}
        if event.type == MOUSEBUTTONUP:
            (mouse_x, mouse_y) = pygame.mouse.get_pos()
            if (mouse_x - config.roll_circle_position[0]) ** 2 + (
                    mouse_y - config.roll_circle_position[1]) ** 2 < config.select_range ** 2:
                return {"protocol": "roll_dice", "button": "up", 'from': self.name}  # 鼠标在摇按钮处抬起
        (mouse_x, mouse_y) = (0, 0)  # 重置鼠标位置记录
        return False  # 鼠标点击其他位置

    # 计算本次各项分数
    def count_score(self):
        self.score_now = np.zeros(17, dtype=int)
        dice1 = list(self.dice)  # 复制骰子数列, 以防下列操作影响原数列
        dice_set = set(dice1)  # 骰子点数集合
        dice_sum = sum(dice1)  # 骰子点数之和
        dice1.sort()  # 骰子点数重排
        # 1到6单独点数分数
        for i in range(5):
            for j in range(6):
                if dice1[i] == j + 1:
                    self.score_now[j] += j + 1
        # 三条
        if dice1[0] == dice1[2] or dice1[1] == dice1[3] or dice1[2] == dice1[4]:
            self.score_now[8] = dice_sum
        # 四条
        if dice1[0] == dice1[3] or dice1[1] == dice1[4]:
            self.score_now[9] = dice_sum
        # 葫芦
        if dice1[0] == dice1[2] and dice1[3] == dice1[4] or \
                dice1[0] == dice1[1] and dice1[2] == dice1[4]:
            self.score_now[10] = 25
        # 小顺
        if dice_set & {1, 2, 3, 4} == {1, 2, 3, 4} or \
                dice_set & {2, 3, 4, 5} == {2, 3, 4, 5} or \
                dice_set & {3, 4, 5, 6} == {3, 4, 5, 6}:
            self.score_now[11] = 30
        # 大顺
        if dice_set & {1, 2, 3, 4, 5} == {1, 2, 3, 4, 5} or \
                dice_set & {2, 3, 4, 5, 6} == {2, 3, 4, 5, 6}:
            self.score_now[12] = 40
        # 游艇
        if dice1[0] == dice1[4]:
            self.score_now[13] = 50
        # 全计
        self.score_now[14] = dice_sum

    # 选择骰子
    def select_dice(self, protocol):
        e = protocol['button']
        if -1 < e < 5:
            if 0 < self.roll_time < 3:
                if e not in self.selected_dice:  # 如果e不在已选择的骰子中，则加入e
                    self.selected_dice.append(e)
                    logger.info('select dice {}'.format(e + 1))
                else:
                    self.selected_dice.remove(e)  # 如果e在已选择的骰子中，则去掉e
                    logger.info("remove dice {}".format(e + 1))
                return True

    # 摇骰子
    def roll_dice(self, protocol):
        logger.debug(protocol)
        e = protocol['button']
        self.play_music(get_path('resource/audio/roll_dice.mp3'), 1, 1)
        if protocol['from'] == self.name:
            if e == 'down':
                pygame.draw.circle(self.screen, config.green, config.roll_circle_position, 2 * config.roll_font / 3)
                self.screen.blit(font_roll.render('摇', True, config.red), config.roll_position)
                pygame.display.update()
            if e == 'up':
                if self.roll_time == 0:  # 如果是本回合第一次摇，那么随机化五个骰子
                    for i in range(5):
                        self.dice[i] = random.randint(1, 6)

                elif len(self.selected_dice) != 0:  # 如果不是本回合第一次摇，且已经选择了一些骰子，随机化选择的骰子
                    for j in self.selected_dice:
                        self.dice[j] = random.randint(1, 6)

                else:
                    self.draw_board()
                    return
                self.roll_time += 1
                self.selected_dice = []
                self.count_score()
                protocol.update({'dice': self.dice})
                return True
        elif protocol['from'] != self.name:
            logger.debug("opponent: {}, dice: {}".format(protocol['from'], protocol['dice']))
            self.dice = protocol['dice']
            self.roll_time += 1
            self.selected_dice = []
            self.count_score()
            return True

    # 选择分数
    def record_score(self, protocol):
        e = protocol['button']
        if protocol['from'] == self.player and self.roll_time != 0 and not self.score_record[self.player][e][
            "recorded"]:
            #  如果来自于当前玩家, 并且已经摇过一次骰子，并且此位置未记录分数
            logger.info('Turn = {}, {} score {} = {}'.format(self.game_turn, self.player, e, self.score_now[e]))
            self.score_record[self.player][e]["score"] = self.score_now[e]
            self.score_record[self.player][e]["recorded"] = True
            upper_half = 0
            for ii in [6, 7, 15, 16]:
                self.score_record[self.player][ii]["score"] = 0
            for j in range(6):
                upper_half += self.score_record[self.player][j]["score"]
            if upper_half > 62:
                self.score_record[self.player][6]["score"] = 35
                self.score_record[self.player][7]["score"] = upper_half + 35
            else:
                self.score_record[self.player][6]["score"] = upper_half - 63
                self.score_record[self.player][7]["score"] = upper_half
            self.score_record[self.player][6]["recorded"] = True
            for k in range(7):
                self.score_record[self.player][15]["score"] += self.score_record[self.player][k + 8]["score"]
            self.score_record[self.player][16]["score"] = self.score_record[self.player][7]["score"] + \
                                                          self.score_record[self.player][15]["score"]
            self.player = [key for key, value in self.player_list.items() if
                           value == (self.player_list[self.player] + 1) % len(self.player_list)]  # 交换玩家
            self.game_turn += 1  # 回合数+1
            self.roll_time = 0  # 摇骰子次数变为0
            self.dice = [0, 0, 0, 0, 0]  # 初始化五个骰子
            self.score_now = np.zeros(17, dtype=int)  # 初始化临时分数
            return True

    # 判断胜负
    def game_over(self):
        if self.game_turn > 13 * len(self.player_list):
            # if self.score_record[self.name][16]["score"] > self.score_record['opponent'][16]["score"]:
            #     self.draw_text('你赢了！', config.x_length / 2, config.y_length / 2, 50)
            # elif self.score_record[self.name][16]["score"] < self.score_record['opponent'][16]["score"]:
            #     self.draw_text('你输了！', config.x_length / 2, config.y_length / 2, 50)
            # else:
            self.draw_text('游戏结束', config.x_length / 2, config.y_length / 2, 50)
            while True:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()

    # 处理登录信息
    def login(self, protocol):
        if 'login_state' in protocol:
            logger.info("登录成功")
            self.order = protocol['order']
            self.player_list[self.name] = self.order
            self.login_state = True
        if 'opponent' in protocol and protocol['opponent'] not in self.player_list:
            self.player_list.update({protocol['opponent']: protocol['order']})
            self.score_record.update({protocol['opponent']: {}})
            for i in range(17):     # 创建dict对象来记录该玩家的分数，False表示未计分
                self.score_record[protocol['opponent']].update(
                    {i: {"score": 0, "recorded": False}})
            for j in [7, 15, 16]:   # 对于Bonus和总分项不需要点击登记，而是实时计算
                self.score_record[protocol['opponent']][j]["recorded"] = True
            logger.info('player {} joined the game'.format(protocol['opponent']))
        if 'begin' in protocol:
            self.player = [key for key, value in self.player_list.items() if value == 0][0]
            logger.info('game begins, self.player = {}'.format(self.player))
            self.draw_board()

    @staticmethod
    def play_music(path, volume, time):
        logger.debug('play music:{} {} time'.format(path, "∞" if time == -1 else time))
        music = pygame.mixer.Sound(get_path(path))
        music.set_volume(volume)
        music.play(time, 0, 0)

    def call_method(self, data):
        if type(data) == bytes:
            data = data.decode()
            if '#' in data:
                data_list = data.split('#')
                for per_data in data_list:
                    if len(per_data) == 0:
                        continue
                    data1 = json.loads(per_data)
                    protocol = data1['protocol']
                    if not hasattr(self, protocol):
                        return None
                    method = getattr(self, protocol)
                    if method(data1):
                        self.draw_board()
                        return True
            else:
                data1 = json.loads(data.decode())
                protocol = data1['protocol']
                if not hasattr(self, protocol):
                    return None
                method = getattr(self, protocol)
                if method(data1):
                    self.draw_board()
                    return True
        # 根据协议中的protocol字段，直接调用相应的函数处理

    def recv_data(self):
        while True:
            try:
                data = s.recv(4096)  # 只做粘包不做分包处理。
                if len(data) == 0:
                    logger.info('有玩家离线')
                    s.close()
                    break
                self.call_method(data)
                # 将字节流转成字符串
            except BlockingIOError:
                pass

    def send_data(self):
        # 向服务端发送登录信息
        protocol = str({"protocol": "login", "name": self.name, "player_num": self.player_num})
        s.send(protocol.encode())
        # 向服务端发送本地操作信息
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    logger.info('主动退出')
                    pygame.quit()
                    sys.exit()
                if self.player == self.name:
                    logger.info('new event: {}'.format(event))
                    protocol = self.check_event(event)
                    logger.info('local protocol: {}'.format(protocol))
                    if protocol:
                        if self.call_method(protocol):
                            s.send(str(protocol).encode())
                self.draw_text('游戏运行中', config.x_length / 2, config.y_length / 2, 10)
            # if self.player == self.name:
            #     self.draw_board()
            #     for event in pygame.event.get():
            #         protocol = self.check_event(event)
            #         if protocol:
            #             if self.call_method(protocol):
            #                 s.send(str(protocol).encode())
            # elif self.player and self.player != self.name:
            #     self.draw_board()
            #     for event in pygame.event.get():
            #         if event.type == QUIT:
            #             logger.info('主动退出')
            #             pygame.quit()
            #             sys.exit()
            #         if self.player == self.name:
            #             break
            # else:
            #     pass
            self.game_over()


def main():
    # logger.info("请输入昵称:")
    # p_name = input()
    # logger.info("请输入玩家数量:")
    # p_number = input()
    p_name = 'aoto'
    p_number = '2'
    y = Ytz(p_name, p_number)
    threads = list()
    threads.append(Thread(target=y.send_data))
    threads.append(Thread(target=y.recv_data))
    for thread in threads:
        thread.start()


if __name__ == "__main__":
    main()
