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
import config
import socket
from yachtDice import Ytz

pygame.display.set_caption('游艇骰子')
pygame.init()
font_roll = pygame.font.Font('./font/simhei.ttf', config.roll_font)
font_score = pygame.font.Font('./font/simhei.ttf', 20)
font_player = pygame.font.Font('./font/simhei.ttf', 28)
font_20 = pygame.font.Font('./font/simhei.ttf', 20)
font_25 = pygame.font.Font('./font/simhei.ttf', 25)
font_30 = pygame.font.Font('./font/simhei.ttf', 30)


# class Ytz(object):
#     def __init__(self):
#         self.screen = pygame.display.set_mode((config.x_length, config.y_length))
#         self.bg_color = config.white
#         self.bg_picture = pygame.image.load('./images/background.jpg')
#         self.img = [pygame.image.load('./images/0.jpg'), pygame.image.load('./images/1.png'),
#                     pygame.image.load('./images/2.png'), pygame.image.load('./images/3.png'),
#                     pygame.image.load('./images/4.png'), pygame.image.load('./images/5.png'),
#                     pygame.image.load('./images/6.png')]
#         self.name = '大麻'  # 玩家昵称
#         self.order = None  # 玩家顺序
#         self.opponent = None  # 对手玩家
#         self.player = None  # 当前回合玩家
#         self.game_turn = 1  # 回合数
#         self.roll_time = 0  # 本回合摇骰子次数
#         self.dice = np.zeros(5, dtype=int)  # 当前骰子点数
#         self.selected_dice = []  # 选择要摇的骰子
#         self.score_now = np.zeros(17, dtype=int)  # 临时显示本次摇骰子的各项分数
#         self.score_record = {self.name: {}, "opponent": {}}  # 已经记录的分数
#         for i in range(17):  # 创建dict对象来记录两位玩家的分数，False表示未计分
#             self.score_record[self.name].update(
#                 {i: {"score": 0, "recorded": False}})
#             self.score_record["opponent"].update(
#                 {i: {"score": 0, "recorded": False}})
#         for j in [7, 15, 16]:  # 对于Bonus和总分项不需要点击登记，而是实时计算
#             self.score_record[self.name][j]["recorded"] = True
#             self.score_record["opponent"][j]["recorded"] = True
#
#     def draw_board(self):
#         # 显示出五个骰子和摇骰子按钮
#         logger.debug(self)
#         self.screen.fill(self.bg_color)
#         self.screen.blit(self.bg_picture, (0, 100))
#         for i in range(5):
#             self.screen.blit(self.img[self.dice[i]], (i * config.dice_length, 0))
#         pygame.draw.circle(self.screen, config.gray, config.roll_circle_position, 2 * config.roll_font / 3)
#         self.screen.blit(font_roll.render('摇', True, config.red), config.roll_position)
#         # 显示出游戏玩家
#         self.screen.blit(font_player.render('回合{}/13'.format(math.ceil(self.game_turn / 2)), True, config.black),
#                          (42, 105))
#         self.screen.blit(font_25.render('{}/3'.format(self.roll_time), True, config.black), (531, 75))
#         if self.player == self.name:
#             player_color = [config.red, config.black]
#         else:
#             player_color = [config.black, config.red]
#         if self.order == 0:
#             player_location = [config.player_1_location, config.player_2_location]
#         else:
#             player_location = [config.player_2_location, config.player_1_location]
#         self.screen.blit(font_player.render(self.name, True, player_color[0]),
#                          (player_location[0] - 30, config.dice_length + 5))
#         self.screen.blit(font_player.render(self.opponent, True, player_color[1]),
#                          (player_location[1] - 30, config.dice_length + 5))
#         # 显示出各项分数
#         score_location = [config.player_1_location, config.player_2_location]
#         for player, data in self.score_record.items():
#             if player == self.player:
#                 i = 0 if self.player == self.name and self.order == 0 or self.player != self.name and self.order == 1 else 1
#                 for key, value in data.items():
#                     if self.score_record[player][key]["recorded"]:
#                         single_score = font_score.render(str(self.score_record[player][key]["score"]), True,
#                                                          config.black)
#                         self.screen.blit(single_score, (score_location[i],
#                                                         config.dice_length + config.list_y_length + config.score_font / 2 + key * config.list_y_length))
#                     if not self.score_record[player][key]["recorded"]:
#                         single_score = font_score.render(str(self.score_now[key]), True, config.gray)
#                         self.screen.blit(single_score, (score_location[i],
#                                                         config.dice_length + config.list_y_length + config.score_font / 2 + key * config.list_y_length))
#             else:
#                 i = 1 if self.player == self.name and self.order == 0 or self.player != self.name and self.order == 1 else 0
#                 for key, value in data.items():
#                     if self.score_record[player][key]["recorded"]:
#                         single_score = font_score.render(str(self.score_record[player][key]["score"]), True,
#                                                          config.black)
#                         self.screen.blit(single_score, (score_location[i],
#                                                         config.dice_length + config.list_y_length + config.score_font / 2 + key * config.list_y_length))
#         # 显示出屏幕左边的得分列表
#         for j in range(17):
#             if j == 7 or j == 15:
#                 score_list = font_25.render(config.score_list[j], True, config.black)
#                 self.screen.blit(score_list, (60, 6 + config.dice_length + (j + 1) * config.list_y_length))
#             elif j == 16:
#                 score_list = font_30.render(config.score_list[j], True, config.black)
#                 self.screen.blit(score_list, (70, 4 + config.dice_length + (j + 1) * config.list_y_length))
#             else:
#                 score_list = font_20.render(config.score_list[j], True, config.black)
#                 self.screen.blit(score_list, (80, 8 + config.dice_length + (j + 1) * config.list_y_length))
#         # 用直线将各项分隔开
#         for i in range(18):
#             pygame.draw.line(self.screen, config.black, (0, config.dice_length + config.list_y_length * i),
#                              (config.x_length, config.dice_length + config.list_y_length * i), 2)
#         pygame.draw.line(self.screen, config.black, (config.list_x_length, config.dice_length),
#                          (config.list_x_length, config.y_length),
#                          3)
#         pygame.draw.line(self.screen, config.black,
#                          (config.list_x_length + config.list_player_length, config.dice_length),
#                          (config.list_x_length + config.list_player_length, config.y_length), 3)
#         for k in self.selected_dice:
#             pygame.draw.circle(self.screen, config.red, (k * 100 + 50, 50), 50, 3)
#         pygame.display.update()
#
#     # 弹出提示
#     def draw_text(self, text, xx, yy, size):
#         pygame.font.init()
#         fontObj = pygame.font.Font('./font/simhei.ttf', size)
#         textSurfaceObj = fontObj.render(text, True, config.white, config.black)
#         textRectObj = textSurfaceObj.get_rect()
#         textRectObj.center = (xx, yy)
#         self.screen.blit(textSurfaceObj, textRectObj)
#         pygame.display.update()
#
#     # 检查事件
#     def check_event(self, event):
#         if event.type == QUIT:
#             return {"protocol": 'offline', "button": 'quit', 'from': self.name}
#         if event.type == MOUSEBUTTONDOWN:  # 鼠标点击，根据点击位置返回数字
#             (mouse_x, mouse_y) = pygame.mouse.get_pos()
#             for i in range(5):
#                 if (mouse_x - (i * config.dice_length + config.dice_length / 2)) ** 2 + (
#                         mouse_y - config.dice_length / 2) ** 2 < config.select_range ** 2:
#                     return {"protocol": 'select_dice', "button": i, 'from': self.name}
#             if (mouse_x - config.roll_circle_position[0]) ** 2 + (
#                     mouse_y - config.roll_circle_position[1]) ** 2 < config.select_range ** 2:
#                 return {"protocol": "roll_dice", "button": "down", 'from': self.name}  # 鼠标在摇按钮处点下
#             for i in range(17):
#                 if (mouse_x - config.player_1_location) ** 2 + (
#                         mouse_y - (config.dice_length + config.list_y_length * 1.5 + i * config.list_y_length)) ** 2 < (
#                         config.list_y_length / 2) ** 2:
#                     return {"protocol": "record_score", "button": i + 6, 'from': self.name}
#                 if (mouse_x - config.player_2_location) ** 2 + (
#                         mouse_y - (config.dice_length + config.list_y_length * 1.5 + i * config.list_y_length)) ** 2 < (
#                         config.list_y_length / 2) ** 2:
#                     return {"protocol": "record_score", "button": i + 23, 'from': self.name}
#             (mouse_x, mouse_y) = (0, 0)  # 重置鼠标位置记录
#         if event.type == MOUSEBUTTONUP:
#             (mouse_x, mouse_y) = pygame.mouse.get_pos()
#             if (mouse_x - config.roll_circle_position[0]) ** 2 + (
#                     mouse_y - config.roll_circle_position[1]) ** 2 < config.select_range ** 2:
#                 return {"protocol": "roll_dice", "button": "up", 'from': self.name}  # 鼠标在摇按钮处抬起
#         return False  # 鼠标点击其他位置
#
#     # 计算本次分数
#     def count_score(self):
#         self.score_now = np.zeros(17, dtype=int)
#         dice1 = list(self.dice)  # 复制骰子数列, 以防下列操作影响原数列
#         dice_set = set(dice1)  # 骰子点数集合
#         dice_sum = sum(dice1)  # 骰子点数之和
#         dice1.sort()  # 骰子点数重排
#         # 1到6单独点数分数
#         for i in range(5):
#             for j in range(6):
#                 if dice1[i] == j + 1:
#                     self.score_now[j] += j + 1
#         # 三条
#         if dice1[0] == dice1[2] or dice1[1] == dice1[3] or dice1[2] == dice1[4]:
#             self.score_now[8] = dice_sum
#         # 四条
#         if dice1[0] == dice1[3] or dice1[1] == dice1[4]:
#             self.score_now[9] = dice_sum
#         # 葫芦
#         if dice1[0] == dice1[2] and dice1[3] == dice1[4] or \
#                 dice1[0] == dice1[1] and dice1[2] == dice1[4]:
#             self.score_now[10] = 25
#         # 小顺
#         if dice_set & {1, 2, 3, 4} == {1, 2, 3, 4} or \
#                 dice_set & {2, 3, 4, 5} == {2, 3, 4, 5} or \
#                 dice_set & {3, 4, 5, 6} == {3, 4, 5, 6}:
#             self.score_now[11] = 30
#         # 大顺
#         if dice_set & {1, 2, 3, 4, 5} == {1, 2, 3, 4, 5} or \
#                 dice_set & {2, 3, 4, 5, 6} == {2, 3, 4, 5, 6}:
#             self.score_now[12] = 40
#         # 游艇
#         if dice1[0] == dice1[4]:
#             self.score_now[13] = 50
#         # 全计
#         self.score_now[14] = dice_sum
#
#     # 选择骰子
#     def select_dice(self, protocol):
#         e = protocol['button']
#         if -1 < e < 5:
#             if 0 < self.roll_time < 3:
#                 if e not in self.selected_dice:  # 如果e不在已选择的骰子中，则加入e
#                     self.selected_dice.append(e)
#                     logger.info('select dice {}'.format(e + 1))
#                 else:
#                     self.selected_dice.remove(e)  # 如果e在已选择的骰子中，则去掉e
#                     logger.info("remove dice {}".format(e + 1))
#                 return True
#
#     # 摇骰子
#     def roll_dice(self, protocol):
#         e = protocol['button']
#         if protocol['from'] == self.name:
#             if e == 'down':
#                 pygame.draw.circle(self.screen, config.green, config.roll_circle_position, 2 * config.roll_font / 3)
#                 self.screen.blit(font_roll.render('摇', True, config.red), config.roll_position)
#                 pygame.display.update()
#             if e == 'up':
#                 if self.roll_time == 0:  # 如果是本回合第一次摇，那么随机化五个骰子
#                     for i in range(5):
#                         self.dice[i] = random.randint(1, 6)
#
#                 elif len(self.selected_dice) != 0:  # 如果不是本回合第一次摇，且已经选择了一些骰子，随机化选择的骰子
#                     for j in self.selected_dice:
#                         self.dice[j] = random.randint(1, 6)
#
#                 else:
#                     self.draw_board()
#                     return
#                 pygame.mixer.music.load('./audio/roll_dice.mp3')
#                 pygame.mixer.music.play()
#                 self.roll_time += 1
#                 self.selected_dice = []
#                 self.count_score()
#                 return True
#         elif protocol['from'] == 'opponent':
#             self.dice = protocol['dice']
#             self.count_score()
#
#     # 选择分数
#     def record_score(self, protocol):
#         e = protocol['button']
#         if (protocol['from'] == self.name) and (self.order*17 + 5 < e < self.order*17 + 23) or protocol['from'] == 'opponent':
#             i = e - 6 if e < 23 else e - 23
#             if not self.score_record[self.player][i]["recorded"]:
#                 #  如果当前玩家位置和点击位置相一致, 并且此位置未记录分数的话
#                 logger.info('Turn = {}, {} score {} = {}'.format(self.game_turn, self.player, e, self.score_now[i]))
#                 self.score_record[self.player][i]["score"] = self.score_now[i]
#                 self.score_record[self.player][i]["recorded"] = True
#                 upper_half = 0
#                 for ii in [6, 7, 15, 16]:
#                     self.score_record[self.player][ii]["score"] = 0
#                 for j in range(6):
#                     upper_half += self.score_record[self.player][j]["score"]
#                 if upper_half > 62:
#                     self.score_record[self.player][6]["score"] = 35
#                     self.score_record[self.player][7]["score"] = upper_half + 35
#                 else:
#                     self.score_record[self.player][6]["score"] = upper_half - 63
#                     self.score_record[self.player][7]["score"] = upper_half
#                 self.score_record[self.player][6]["recorded"] = True
#                 for k in range(7):
#                     self.score_record[self.player][15]["score"] += self.score_record[self.player][k + 8]["score"]
#                 self.score_record[self.player][16]["score"] = self.score_record[self.player][7]["score"] + \
#                                                               self.score_record[self.player][15]["score"]
#                 self.player = self.name if (self.player == 'opponent') else 'opponent'  # 交换玩家
#                 self.game_turn += 1  # 回合数+1
#                 self.roll_time = 0  # 摇骰子次数变为0
#                 self.dice = np.zeros(5, dtype=int)  # 初始化五个骰子
#                 self.score_now = np.zeros(17, dtype=int)  # 初始化临时分数
#                 return True
#
#     # 判断胜负
#     def game_over(self):
#         if self.game_turn > 26:
#             if self.score_record[self.name][16]["score"] > self.score_record['opponent'][16]["score"]:
#                 self.draw_text('你赢了！', config.x_length / 2, config.y_length / 2, 50)
#             elif self.score_record[self.name][16]["score"] < self.score_record['opponent'][16]["score"]:
#                 self.draw_text('你输了！', config.x_length / 2, config.y_length / 2, 50)
#             else:
#                 self.draw_text('平局了！', config.x_length / 2, config.y_length / 2, 50)
#             while True:
#                 for event in pygame.event.get():
#                     if event.type == QUIT:
#                         pygame.quit()
#                         sys.exit()
#
#     # 处理登录信息
#     def login(self, protocol):
#         if 'order' in protocol:
#             logger.info('order:{}'.format(protocol['order']))
#             self.order = protocol.get('order', None)
#         if 'opponent' in protocol:
#             self.opponent = protocol['opponent']
#             self.player = [self.name, 'opponent'][self.order]
#         return True
#
#     def protocol_handler(self, protocol):
#         protocol_name = protocol['protocol']
#         if not hasattr(self, protocol_name):
#             return None
#         # 调用与协议同名的方法
#         method = getattr(self, protocol_name)
#         if method(protocol):
#             self.draw_board()
#             return True
#
#     def run(self):
#         # 建立socket连接
#         s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         s.connect(('127.0.0.1', 6666))
#         s.setblocking(0)
#         # 向服务端发送登录信息
#         login_data = str({"protocol": "login", "name": self.name})
#         s.send(login_data.encode())
#         try:
#             while True:
#                 try:
#                     data = s.recv(4096)  # 只做粘包不做分包处理。
#                     if len(data) == 0:
#                         logger.info('有玩家离线')
#                         s.close()
#                         break
#                     # 将字节流转成字符串
#                     protocol_str = data.decode()
#                     # 处理每一个协议,最后一个是空字符串，不用处理它
#                     protocol = json.loads(protocol_str)
#                     # 根据协议中的protocol字段，直接调用相应的函数处理
#                     self.protocol_handler(protocol)
#                 except:
#                     pass
#                 if self.player == self.name:
#                     for event in pygame.event.get():
#                         protocol = self.check_event(event)
#                         if protocol:
#                             if self.protocol_handler(protocol):
#                                 s.send(str(protocol).encode())
#         except:
#             s.close()
#             logger.info('服务器发送的数据异常：' + bytes.decode() + '\n' + '已强制下线，详细原因请查看日志文件')


if __name__ == "__main__":
    y = Ytz("seed")
    y.run()
