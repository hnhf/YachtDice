# -*- coding: utf-8 -*-
"""
Created on Thu Jul  1 17:14:09 2021

@author: Fan
"""
import random

import numpy as np
import pygame
from pygame.locals import *

import config

pygame.display.set_caption('游艇骰子')
pygame.init()
# 显示数字
font_color = (0, 0, 0)
font_small = pygame.font.Font('./font/simhei.ttf', 16)
font_middle = pygame.font.Font('./font/simhei.ttf', 28)
font_big = pygame.font.Font('./font/simhei.ttf', 65)


class Ytz(object):
    def __init__(self):
        self.screen = pygame.display.set_mode((config.x_length, config.y_length))
        self.bg_color = config.bg_color
        self.img = [pygame.image.load('./images/1.png'), pygame.image.load('./images/2.png'),
                    pygame.image.load('./images/3.png'),
                    pygame.image.load('./images/4.png'), pygame.image.load('./images/5.png'),
                    pygame.image.load('./images/6.png')]
        self.dice = config.dice

        self.score_now_1 = np.zeros(17, dtype=int)  # 本轮骰子的各项分数
        self.score_now_2 = np.zeros(17, dtype=int)
        self.score_record_1 = np.zeros(17, dtype=int)  # 已经产生的分数
        self.score_record_2 = np.zeros(17, dtype=int)

        self.selected_dice = []
        self.roll_time = config.roll_time

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

    #
    # def draw_again():
    #     for i in range(5):
    #         self.screen.blit(img[dice[i]], (i * 100, 0))
    #     score_now = count_score()
    #     if player == 1:
    #         location = player_A_location
    #     else:
    #         location = player_B_location
    #     for j in range(17):
    #         if score_record_1[j] != -1:
    #             single_score_1 = font_small.render(str(score_now[j]), True, font_color)
    #             self.screen.blit(single_score_1, (location, 160 + j * 40))
    #     pygame.display.update()
    #
    #
    # def count_score():
    #     score_now = np.zeros(17, dtype=int)
    #     dice1 = dice[:]  # 复制骰子数列
    #     dice_set = set(dice)  # 骰子点数集合
    #     dice_sum = sum(dice)  # 骰子点数之和
    #     dice1.sort()  # 骰子点数重排
    #     # 1到6单独点数分数
    #     for dice_i in range(5):
    #         for score_i in range(5):
    #             for point_i in range(6):
    #                 if dice1[dice_i] == point_i + 1:
    #                     score_now[score_i] += point_i + 1
    #     # 三条
    #     if dice1[0] == dice1[2] or dice1[1] == dice1[3] or dice1[2] == dice1[4]:
    #         score_now[9] = dice_sum
    #     # 四条
    #     if dice1[0] == dice1[3] or dice1[1] == dice1[4]:
    #         score_now[10] = dice_sum
    #     # 葫芦
    #     if dice1[0] == dice1[2] and dice1[3] == dice1[4] or \
    #             dice1[0] == dice1[1] and dice1[2] == dice1[4]:
    #         score_now[11] = 25
    #     # 小顺
    #     if dice_set & {1, 2, 3, 4} == {1, 2, 3, 4} or \
    #             dice_set & {2, 3, 4, 5} == {2, 3, 4, 5} or \
    #             dice_set & {3, 4, 5, 6} == {3, 4, 5, 6}:
    #         score_now[12] = 30
    #     # 大顺
    #     if dice_set & {1, 2, 3, 4, 5} == {1, 2, 3, 4, 5} or \
    #             dice_set & {2, 3, 4, 5, 6} == {2, 3, 4, 5, 6}:
    #         score_now[13] = 40
    #     # 游艇
    #     if dice1[0] == dice1[4]:
    #         score_now[14] = 50
    #     # 全计
    #     score_now[15] = dice_sum
    #     return score_now
    #
    # while True:
    #     draw_board()
    #

    # 选择骰子
    def select_dice(self, event):
        # 用这个
        if self.roll_time < 3:
            if event.type == MOUSEBUTTONDOWN:
                (mouse_x, mouse_y) = pygame.mouse.get_pos()
                for i in range(5):
                    if (mouse_x - (i * 100 + 50)) ^ 2 + (mouse_y - 50) ^ 2 < config.select_range ^ 2 and (
                            i + 1) not in self.selected_dice:
                        self.selected_dice.append(i + 1)
                    if (mouse_x - (i * 100 + 50)) ^ 2 + (mouse_y - 50) ^ 2 < config.select_range ^ 2 and (
                            i + 1) in self.selected_dice:
                        self.selected_dice.remove(i + 1)
                    else:
                        pass

    # 掷骰子
    def roll_dice(self, event):
        if self.roll_time < 3:
            if event.type == MOUSEBUTTONDOWN:
                (mouse_x, mouse_y) = pygame.mouse.get_pos()
                if ((mouse_x - 544) ^ 2 + (mouse_y - 48) ^ 2) ^ 0.5 < config.select_range:
                    for i in self.selected_dice:
                        self.dice[i] = random.randint(1, 6)
        selected_dice = []

    def run(self):
        while True:
            for event in pygame.event.get():
                self.select_dice(event)
                self.roll_dice(event)


if __name__ == "__main__":
    y = Ytz()
    y.run()
#
# def draw_dice():
#     for i in range(5):
#         self.screen.blit(img[dice[i]],(50, i*50))
#     pygame.display.update()
#
# #选择分数
# def choose_score(event):
#     if event.type == MOUSEBUTTONDOWN:
#         pos_score = pygame.mouse.get_pos()
#
#
# def game_over():
#     if game_turn == 13:
#         return 1
#     else:
#         return 0
#
# def draw_text(text,x,y,size):
#     pygame.font.init()
#     fontObj = pygame.font.SysFont('SimHei', size)
#     textSurfaceObj = fontObj.render(text, True, white, black)
#     textRectObj = textSurfaceObj.get_rect()
#     textRectObj.center = (x, y)
#     self.screen.blit(textSurfaceObj, textRectObj)
#     pygame.display.update()
#
# #主循环
# draw_board()
#
#
# while True:
#     for event in pygame.event.get():
#         if event.type == QUIT:
#             tcpCliSock.close()
#             pygame.quit()
#             sys.exit()
#         if settable == 1:
#             roll_time = 1
#             roll_dice()
#             if roll_time < 3:
#                 roll_time += 1
#                 roll_dice()
#             else:
#                 if choose_score() = 1:
#                     count_score
#                     draw_text('对手回合', 200, 420, 15)
#                     settable = 0
#
#     draw_dice()
#     if gameover() == 1:
#         draw_text('你赢了！', 200, 420, 15)
#         while True:
#             for event in pygame.event.get():
#                 if event.type == QUIT:
#                     pygame.quit()
#                     sys.exit()
#     elif gameover() == 2:
#         draw_text('你输了！', 200, 420, 15)
#         while True:
#             for event in pygame.event.get():
#                 if event.type == QUIT:
#                     pygame.quit()
#                     sys.exit()
#     elif gameover() == 3:
#         draw_text('平局！', 200, 420, 15)
#         while True:
#             for event in pygame.event.get():
#                 if event.type == QUIT:
#                     pygame.quit()
#                     sys.exit()
