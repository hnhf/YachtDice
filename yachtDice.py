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
font_color = config.black
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
            self.screen.blit(self.img[self.dice[i]], (i * 100, 0))
        pygame.draw.circle(self.screen, config.gray, (544, 48), 42)
        roll_cha = font_big.render('摇', True, config.red)
        self.screen.blit(roll_cha, (510, 15))
        players = font_middle.render('玩家', True, font_color)
        player_a = font_middle.render('A', True, font_color)
        player_b = font_middle.render('B', True, font_color)
        self.screen.blit(players, (35, 110))
        self.screen.blit(player_a, (config.player_A_location - 2, 110))
        self.screen.blit(player_b, (config.player_B_location - 2, 110))
        for j in range(17):
            element_1 = font_small.render(config.score_list[j], True, font_color)
            self.screen.blit(element_1, (50, 160 + j * 40))
            single_score_1 = font_small.render(str(self.score_record_1[j]), True, font_color)
            single_score_2 = font_small.render(str(self.score_record_2[j]), True, font_color)
            self.screen.blit(single_score_1, (config.player_A_location, 160 + j * 40))
            self.screen.blit(single_score_2, (config.player_B_location, 160 + j * 40))
        pygame.draw.line(self.screen, config.black, (0, 100), (config.x_length, 100), 3)
        pygame.draw.line(self.screen, config.black, (0, 100), (config.x_length, 100), 3)
        pygame.draw.line(self.screen, config.black, (0, 150), (config.x_length, 150), 3)
        pygame.draw.line(self.screen, config.gray, (0, 430), (config.x_length, 430), 3)
        pygame.draw.line(self.screen, config.gray, (0, 470), (config.x_length, 470), 3)
        pygame.draw.line(self.screen, config.gray, (0, 750), (config.x_length, 750), 3)
        pygame.draw.line(self.screen, config.black, (0, 790), (config.x_length, 790), 3)
        pygame.draw.line(self.screen, config.gray, (150, 100), (150, config.y_length), 3)
        pygame.draw.line(self.screen, config.gray, (375, 100), (375, config.y_length), 3)
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
                if (mouse_x - (i * 100 + 50)) ^ 2 + (mouse_y - 50) ^ 2 < config.select_range ^ 2:
                    return i
            if (mouse_x - 544) ^ 2 + (mouse_y - 48) ^ 2 < config.select_range ^ 2:
                return 5
            for i in range(17):
                if (mouse_x - config.player_A_location) ^ 2 + (mouse_y - (160 + i * 40)) ^ 2 < 20 ^ 2:
                    return i + 6
                if (mouse_x - config.player_A_location) ^ 2 + (mouse_y - (160 + i * 40)) ^ 2 < 20 ^ 2:
                    return i + 23

    # 重新显示
    def draw_again(self):
        for i in range(5):
            self.screen.blit(self.img[self.dice[i]], (i * 100, 0))
        score_now = self.count_score()
        if self.player == 1:
            location = config.player_A_location
        else:
            location = config.player_B_location
        for j in range(17):
            if self.score_record_1[j] != -1:
                single_score_1 = font_small.render(str(score_now[j]), True, font_color)
                self.screen.blit(single_score_1, (location, 160 + j * 40))
        pygame.display.update()

    # 重画骰子
    def draw_dice(self):
        for i in range(5):
            self.screen.blit(self.img[self.dice[i]], (50, i * 50))
        pygame.display.update()

    # 计算本次分数
    def count_score(self):
        score_now = np.zeros(17, dtype=int)
        dice1 = self.dice[:]  # 复制骰子数列
        dice_set = set(self.dice)  # 骰子点数集合
        dice_sum = sum(self.dice)  # 骰子点数之和
        dice1.sort()  # 骰子点数重排
        # 1到6单独点数分数
        for dice_i in range(5):
            for score_i in range(5):
                for point_i in range(6):
                    if dice1[dice_i] == point_i + 1:
                        score_now[score_i] += point_i + 1
        # 三条
        if dice1[0] == dice1[2] or dice1[1] == dice1[3] or dice1[2] == dice1[4]:
            score_now[9] = dice_sum
        # 四条
        if dice1[0] == dice1[3] or dice1[1] == dice1[4]:
            score_now[10] = dice_sum
        # 葫芦
        if dice1[0] == dice1[2] and dice1[3] == dice1[4] or \
                dice1[0] == dice1[1] and dice1[2] == dice1[4]:
            score_now[11] = 25
        # 小顺
        if dice_set & {1, 2, 3, 4} == {1, 2, 3, 4} or \
                dice_set & {2, 3, 4, 5} == {2, 3, 4, 5} or \
                dice_set & {3, 4, 5, 6} == {3, 4, 5, 6}:
            score_now[12] = 30
        # 大顺
        if dice_set & {1, 2, 3, 4, 5} == {1, 2, 3, 4, 5} or \
                dice_set & {2, 3, 4, 5, 6} == {2, 3, 4, 5, 6}:
            score_now[13] = 40
        # 游艇
        if dice1[0] == dice1[4]:
            score_now[14] = 50
        # 全计
        score_now[15] = dice_sum
        return score_now

    # 选择骰子
    def select_dice(self, selected_dice, e):
        if self.roll_time < 3:
            if -1 < e < 5:
                if e not in self.selected_dice:
                    self.selected_dice.append(e)
                if e in self.selected_dice:
                    self.selected_dice.remove(e)
                self.draw_dice()

    # 摇骰子
    def roll_dice(self, e, new_turn=0):
        if new_turn == 1:
            for i in range(5):
                self.dice[i] = random.randint(1, 6)
        if e == 6 & self.roll_time < 3 & len(self.selected_dice) != 0:
            for j in self.selected_dice:
                self.dice[j] = random.randint(1, 6)
        self.selected_dice = []
        self.count_score()
        self.draw_again()

    # 选择分数
    def choose_score(self, e):
        if self.player == 1 & (5 < e < 23) or self.player == 2 & (22 < e < 40):
            if self.player == 1:
                self.score_record_1[e - 6] = self.score_now[e - 6]
                self.player = 2
            if self.player == 2:
                self.score_record_2[e - 23] = self.score_now[e - 23]
                self.player = 1
            self.game_turn += 1
            self.roll_dice(e, 1)

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
                self.select_dice(self.selected_dice, e)  # 选择骰子
                self.roll_dice(e)  # 摇骰子
                self.choose_score(e)  # 选择分数
                self.game_over()  # 判断胜负


if __name__ == "__main__":
    y = Ytz()
    y.run()
