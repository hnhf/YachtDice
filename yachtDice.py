# -*- coding: utf-8 -*-
"""
Created on Thu Jul  1 17:14:09 2021

@author: Fan
"""
import random
import sys
import numpy as np
import pygame
from pygame.locals import *
from loguru import logger
import config

pygame.display.set_caption('游艇骰子')
pygame.init()
font_roll = pygame.font.Font('C:/Windows/Fonts/simhei.ttf', 65)
font_score = pygame.font.Font('C:/Windows/Fonts/simhei.ttf', 16)
font_player = pygame.font.Font('C:/Windows/Fonts/simhei.ttf', 28)
font_20 = pygame.font.Font('C:/Windows/Fonts/simhei.ttf', 20)
font_25 = pygame.font.Font('C:/Windows/Fonts/simhei.ttf', 25)
font_30 = pygame.font.Font('C:/Windows/Fonts/simhei.ttf', 30)


class Ytz(object):
    def __init__(self):
        self.screen = pygame.display.set_mode((config.x_length, config.y_length))
        self.bg_color = config.white
        self.img = [pygame.image.load('./images/1.png'), pygame.image.load('./images/2.png'),
                    pygame.image.load('./images/3.png'),
                    pygame.image.load('./images/4.png'), pygame.image.load('./images/5.png'),
                    pygame.image.load('./images/6.png')]
        self.dice = [1, 2, 3, 4, 5]
        self.score_now = np.zeros(17, dtype=int)  # 临时显示本次摇骰子的各项分数
        self.score_record = {"player_1": {}, "player_2": {}}  # 已经记录的分数
        for i in range(17):  # 创建dict对象来记录两位玩家的分数，False表示未计分
            self.score_record["player_1"].update(
                {i: {"score": 0, "recorded": False, "location": config.player_1_location}})
            self.score_record["player_2"].update(
                {i: {"score": 0, "recorded": False, "location": config.player_2_location}})
        for j in [7, 15, 16]:  # 对于Bonus和总分项不需要点击登记，而是实时计算
            self.score_record["player_1"][j]["recorded"] = True
            self.score_record["player_2"][j]["recorded"] = True
        self.player = "player_1"  # 游戏初始玩家，之后将在“player_1"和"player_2"之间交替
        self.game_turn = 1  # 回合数
        self.roll_time = 0  # 本回合摇骰子次数
        self.selected_dice = []  # 选择要摇的骰子

    def draw_board(self):
        # 显示出五个骰子和摇骰子按钮
        self.screen.fill(self.bg_color)
        for i in range(5):
            self.screen.blit(self.img[self.dice[i] - 1], (i * 100, 0))
        pygame.draw.circle(self.screen, config.gray, (544, 48), 42)
        self.screen.blit(font_roll.render('摇', True, config.red), (510, 15))
        # 显示出游戏玩家
        self.screen.blit(font_player.render('玩家', True, config.black), (35, 110))
        self.screen.blit(font_player.render('A', True, config.black), (config.player_1_location - 2, 110))
        self.screen.blit(font_player.render('B', True, config.black), (config.player_2_location - 2, 110))
        # 显示出各项分数
        for player, data in self.score_record.items():
            if player == self.player:
                for key, value in data.items():
                    if self.score_record[player][key]["recorded"]:
                        single_score = font_score.render(str(self.score_record[player][key]["score"]), True,
                                                         config.black)
                        self.screen.blit(single_score, (self.score_record[player][key]["location"], 160 + key * 40))
                    if not self.score_record[player][key]["recorded"]:
                        single_score = font_score.render(str(self.score_now[key]), True, config.blue)
                        self.screen.blit(single_score, (self.score_record[player][key]["location"], 160 + key * 40))
            else:
                for key, value in data.items():
                    if self.score_record[player][key]["recorded"]:
                        single_score = font_score.render(str(self.score_record[player][key]["score"]), True,
                                                         config.black)
                        self.screen.blit(single_score, (self.score_record[player][key]["location"], 160 + key * 40))
        # 显示出屏幕左边的得分列表
        for j in range(16):
            if j == 7 or j == 15:
                score_list = font_25.render(config.score_list[j], True, config.black)
                self.screen.blit(score_list, (50, 160 + j * 40))
            elif j == 16:
                score_list = font_30.render(config.score_list[j], True, config.black)
                self.screen.blit(score_list, (50, 160 + j * 40))
            else:
                score_list = font_20.render(config.score_list[j], True, config.black)
                self.screen.blit(score_list, (50, 160 + j * 40))
        # 用直线将各项分隔开
        pygame.draw.line(self.screen, config.black, (0, 103), (config.x_length, 103), 3)
        pygame.draw.line(self.screen, config.black, (0, 150), (config.x_length, 150), 3)
        pygame.draw.line(self.screen, config.gray, (0, 430), (config.x_length, 430), 3)
        pygame.draw.line(self.screen, config.gray, (0, 470), (config.x_length, 470), 3)
        pygame.draw.line(self.screen, config.gray, (0, 750), (config.x_length, 750), 3)
        pygame.draw.line(self.screen, config.black, (0, 790), (config.x_length, 790), 3)
        pygame.draw.line(self.screen, config.gray, (150, 103), (150, config.y_length), 3)
        pygame.draw.line(self.screen, config.gray, (375, 103), (375, config.y_length), 3)
        pygame.display.update()

    # 弹出提示
    def draw_text(self, text, xx, yy, size):
        pygame.font.init()
        fontObj = pygame.font.Font('C:/Windows/Fonts/simhei.ttf', size)
        textSurfaceObj = fontObj.render(text, True, config.white, config.black)
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.center = (xx, yy)
        self.screen.blit(textSurfaceObj, textRectObj)
        pygame.display.update()

    # 检查事件
    @staticmethod
    def check_event(event):
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:  # 鼠标点击，根据点击位置返回数字
            (mouse_x, mouse_y) = pygame.mouse.get_pos()
            for i in range(5):
                if (mouse_x - (i * 100 + 50)) ** 2 + (mouse_y - 50) ** 2 < config.select_range ** 2:
                    return i
            if (mouse_x - 544) ** 2 + (mouse_y - 48) ** 2 < config.select_range ** 2:
                return 5
            for i in range(17):
                if (mouse_x - config.player_1_location) ** 2 + (mouse_y - (160 + i * 40)) ** 2 < 20 ** 2:
                    return i + 6
                if (mouse_x - config.player_2_location) ** 2 + (mouse_y - (160 + i * 40)) ** 2 < 20 ** 2:
                    return i + 23
            (mouse_x, mouse_y) = (0, 0)  # 重置鼠标位置记录
            return -1  # 鼠标点击其他位置则返回-1

    # 计算本次分数
    def count_score(self):
        self.score_now = np.zeros(17, dtype=int)
        dice1 = self.dice[:]  # 复制骰子数列
        dice_set = set(self.dice)  # 骰子点数集合
        dice_sum = sum(self.dice)  # 骰子点数之和
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
    def select_dice(self, e):
        if -1 < e < 5:
            if self.roll_time < 3:
                if e not in self.selected_dice:  # 如果e不在已选择的骰子中，则加入e
                    self.selected_dice.append(e)
                    pygame.draw.circle(self.screen, config.red, (e * 100 + 50, 50), 50, 3)
                    logger.info('{}select_dice 1'.format(e))
                else:
                    self.selected_dice.remove(e)  # 如果e在已选择的骰子中，则去掉e
                    self.screen.blit(self.img[self.dice[e] - 1], (e * 100, 0))
                    logger.info("当前鼠标点击位置：{}， select dice".format(e))
                pygame.display.update()

    # 摇骰子
    def roll_dice(self, e):
        if e == 5:
            if self.roll_time == 0:             # 如果是本回合第一次摇，那么随机化五个骰子
                for i in range(5):
                    self.dice[i] = random.randint(1, 6)
            elif len(self.selected_dice) != 0:  # 如果不是本回合第一次摇，且已经选择了一些骰子，随机化选择的骰子
                for j in self.selected_dice:
                    self.dice[j] = random.randint(1, 6)
            else:
                return
            self.roll_time += 1
            self.selected_dice = []
            self.count_score()
            self.draw_board()

    # 选择分数
    def record_score(self, e):
        if 5 < e < 40:
            logger.info('Turn = {}, e = {}, player = {}'.format(self.game_turn, e, self.player))
            if (self.player == "player_1") and (5 < e < 23) or (self.player == "player_2") and (22 < e < 40):
                i = e - 6 if e < 23 else e - 23
                if not self.score_record[self.player][i]["recorded"]:
                    #  如果当前玩家位置和点击位置相一致, 并且此位置未记录分数的话
                    self.score_record[self.player][i]["score"] = self.score_now[i]
                    self.score_record[self.player][i]["recorded"] = True
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
                    if self.score_record[self.player][6]["score"] == 35:
                        self.score_record[self.player][16]["score"] = self.score_record[self.player][7]["score"] + \
                                                                      self.score_record[self.player][15]["score"] + 35
                    else:
                        self.score_record[self.player][16]["score"] = self.score_record[self.player][7]["score"] + \
                                                                      self.score_record[self.player][15]["score"]
                    self.player = "player_2" if (self.player == "player_1") else "player_1"  # 交换玩家
                    self.game_turn += 1  # 回合数+1
                    self.roll_time = 0  # 摇骰子次数变为0
                    self.score_now = np.zeros(17, dtype=int)  # 初始化临时分数
                    self.draw_board()

    # 判断胜负
    def game_over(self):
        if self.game_turn > 26:
            if self.score_record["player_1"][16]["score"] > self.score_record["player_2"][16]["score"]:
                self.draw_text('玩家1胜利！', 200, 400, 50)
            elif self.score_record["player_1"][16]["score"] < self.score_record["player_2"][16]["score"]:
                self.draw_text('玩家2胜利！', 200, 400, 50)
            else:
                self.draw_text('平局了！', 200, 400, 50)
            while True:
                for event in pygame.event.get():
                    self.check_event(event)

    def run(self):
        self.draw_board()
        while True:
            for event in pygame.event.get():
                e = self.check_event(event)
                if type(e) == int:
                    self.select_dice(e)  # 选择骰子
                    self.roll_dice(e)  # 摇骰子
                    self.record_score(e)  # 选择分数
                self.game_over()  # 判断胜负


if __name__ == "__main__":
    y = Ytz()
    y.run()
