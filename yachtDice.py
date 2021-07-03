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
import config

pygame.display.set_caption('游艇骰子')
pygame.init()
font_small = pygame.font.Font('C:/Windows/Fonts/simhei.ttf', 16)
font_middle = pygame.font.Font('C:/Windows/Fonts/simhei.ttf', 28)
font_big = pygame.font.Font('C:/Windows/Fonts/simhei.ttf', 65)


class Ytz(object):
    def __init__(self):
        self.screen = pygame.display.set_mode((config.x_length, config.y_length))
        self.bg_color = config.white
        self.img = [pygame.image.load('./images/1.png'), pygame.image.load('./images/2.png'),
                    pygame.image.load('./images/3.png'),
                    pygame.image.load('./images/4.png'), pygame.image.load('./images/5.png'),
                    pygame.image.load('./images/6.png')]
        self.dice = [1, 2, 3, 4, 5]
        self.score_now = np.zeros(17, dtype=int)  # 本次骰子的各项分数
        self.score_record_1 = [i - 1 for i in self.score_now]  # 已经产生的分数
        self.score_record_2 = [i - 1 for i in self.score_now]
        self.player = 1
        self.game_turn = 1
        self.roll_time = 0
        self.selected_dice = []

    def draw_board(self):
        self.screen.fill(self.bg_color)
        for i in range(5):
            self.screen.blit(self.img[self.dice[i] - 1], (i * 100, 0))
        pygame.draw.circle(self.screen, config.gray, (544, 48), 42)
        self.screen.blit(font_big.render('摇', True, config.red), (510, 15))
        self.screen.blit(font_middle.render('玩家', True, config.black), (35, 110))
        self.screen.blit(font_middle.render('A', True, config.black), (config.player_A_location - 2, 110))
        self.screen.blit(font_middle.render('B', True, config.black), (config.player_B_location - 2, 110))
        if self.player == 1:
            for j in range(17):
                if self.score_record_1[j] == -1:
                    single_score_1 = font_small.render(str(self.score_now[j]), True, config.blue)
                    self.screen.blit(single_score_1, (config.player_A_location, 160 + j * 40))
                if self.score_record_1[j] != -1:
                    single_score_1 = font_small.render(str(self.score_record_1[j]), True, config.black)
                    self.screen.blit(single_score_1, (config.player_A_location, 160 + j * 40))
        else:
            for k in range(17):
                if self.score_record_2[k] == -1:
                    single_score_2 = font_small.render(str(self.score_now[k]), True, config.blue)
                    self.screen.blit(single_score_2, (config.player_B_location, 160 + k * 40))
                if self.score_record_2[k] != -1:
                    single_score_2 = font_small.render(str(self.score_record_2[k]), True, config.black)
                    self.screen.blit(single_score_2, (config.player_B_location, 160 + k * 40))
        for j in range(17):
            element_1 = font_small.render(config.score_list[j], True, config.black)
            self.screen.blit(element_1, (50, 160 + j * 40))
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
        if event.type == MOUSEBUTTONDOWN:
            (mouse_x, mouse_y) = pygame.mouse.get_pos()
            for i in range(5):
                if (mouse_x - (i * 100 + 50)) ** 2 + (mouse_y - 50) ** 2 < config.select_range ** 2:
                    return i
            if (mouse_x - 544) ** 2 + (mouse_y - 48) ** 2 < config.select_range ** 2:
                return 5
            for i in range(17):
                if (mouse_x - config.player_A_location) ** 2 + (mouse_y - (160 + i * 40)) ** 2 < 20 ** 2:
                    return i + 6
                if (mouse_x - config.player_B_location) ** 2 + (mouse_y - (160 + i * 40)) ** 2 < 20 ** 2:
                    return i + 23
            (mouse_x, mouse_y) = (0, 0)
            return -1

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
        print('count_score')

    # 选择骰子
    def select_dice(self, e):
        if -1 < e < 5:
            if self.roll_time < 3:
                if e not in self.selected_dice:
                    self.selected_dice.append(e)
                    pygame.draw.circle(self.screen, config.red, (e * 100 + 50, 50), 50, 3)
                    print(self.selected_dice)
                else:
                    self.selected_dice.remove(e)
                    self.screen.blit(self.img[self.dice[e] - 1], (e * 100, 0))
                    print(self.selected_dice)
                pygame.display.update()

    # 摇骰子
    def roll_dice(self, e):
        if e == 5:
            if self.roll_time == 0:
                for i in range(5):
                    self.dice[i] = random.randint(1, 6)
            elif self.roll_time < 3 & len(self.selected_dice) != 0:
                for j in self.selected_dice:
                    self.dice[j] = random.randint(1, 6)
            else:
                return
            self.roll_time += 1
            self.selected_dice = []
            self.count_score()
            self.draw_board()
            print('roll_dice')

    # 选择分数
    def choose_score(self, e):
        if self.player == 1 & (5 < e < 23):
            self.score_record_1[e - 6] = self.score_now[e - 6]
            self.player = 2
        elif self.player == 2 & (22 < e < 40):
            self.score_record_2[e - 23] = self.score_now[e - 23]
            self.player = 1
        else:
            return
        self.game_turn += 1
        self.roll_time = 0
        self.roll_dice(e)
        print('choose_score')

    # 判断胜负
    def game_over(self):
        if self.game_turn > 26:
            if self.score_record_1[16] > self.score_record_2[16]:
                self.draw_text('玩家1胜利！', 200, 400, 15)
            elif self.score_record_1[16] > self.score_record_2[16]:
                self.draw_text('玩家2胜利！', 200, 400, 15)
            else:
                self.draw_text('平局了！', 200, 400, 15)
            while True:
                for event1 in pygame.event.get():
                    self.check_event(event1)

    def run(self):
        self.draw_board()
        while True:
            for event in pygame.event.get():
                e = self.check_event(event)
                if type(e) == int:
                    self.select_dice(e)  # 选择骰子
                    self.roll_dice(e)  # 摇骰子
                    self.choose_score(e)  # 选择分数
                self.game_over()  # 判断胜负


if __name__ == "__main__":
    y = Ytz()
    y.run()
