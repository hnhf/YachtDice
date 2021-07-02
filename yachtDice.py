# -*- coding: utf-8 -*-
"""
Created on Thu Jul  1 17:14:09 2021

@author: Fan
"""
import random
import pygame
import sys
import numpy as np
from pygame.locals import *
from collections import Counter
from time import ctime
import json

# 界面初始化
x_length = 600
y_length = 820
screen = pygame.display.set_mode((x_length, y_length))
pygame.display.set_caption('游艇骰子')
bg_color = (255, 255, 255)
pygame.init()

# 图片导入
img = [pygame.image.load('./images/1.png'), pygame.image.load('./images/2.png'), pygame.image.load('./images/3.png'),
       pygame.image.load('./images/4.png'), pygame.image.load('./images/5.png'), pygame.image.load('./images/6.png')]

# 颜色
white = (255, 255, 255)
gray = (200, 200, 200)
red = (255, 0, 0)
black = (0, 0, 0)

# 其他参数
select_range = 30  # 鼠标点击的有效半径
roll_time = 0  # 摇过的次数

# 分数记录
player = 1  # 当前玩家
player_A_location = 250
player_B_location = 475
dice = [1, 2, 3, 4, 5]
score_now_1 = np.zeros(17, dtype=int)  # 本轮骰子的各项分数
score_now_2 = np.zeros(17, dtype=int)
score_record_1 = np.zeros(17, dtype=int)  # 已经产生的分数
score_record_2 = np.zeros(17, dtype=int)
list_1 = ['1点', '2点', '3点', '4点', '5点', '6点', 'Bonus', '上半区总分', '三条', '四条',
          '葫芦', '小顺', '大顺', '游艇', '全计', '下半区总分', '总分']

# 显示数字
font_color = (0, 0, 0)
font_small = pygame.font.Font('C:/Windows/Fonts/simhei.ttf', 16)
font_middle = pygame.font.Font('C:/Windows/Fonts/simhei.ttf', 28)
font_big = pygame.font.Font('C:/Windows/Fonts/simhei.ttf', 65)


def draw_board():
    screen.fill(bg_color)
    for i in range(5):
        screen.blit(img[dice[i]], (i * 100, 0))
    pygame.draw.circle(screen, gray, (544, 48), 42)
    roll_cha = font_big.render('摇', True, red)
    screen.blit(roll_cha, (510, 15))
    players = font_middle.render('玩家', True, font_color)
    player_a = font_middle.render('A', True, font_color)
    player_b = font_middle.render('B', True, font_color)
    screen.blit(players, (35, 110))
    screen.blit(player_a, (player_A_location - 2, 110))
    screen.blit(player_b, (player_B_location - 2, 110))
    for j in range(17):
        element_1 = font_small.render(list_1[j], True, font_color)
        screen.blit(element_1, (50, 160 + j * 40))
        single_score_1 = font_small.render(str(score_record_1[j]), True, font_color)
        single_score_2 = font_small.render(str(score_record_2[j]), True, font_color)
        screen.blit(single_score_1, (player_A_location, 160 + j * 40))
        screen.blit(single_score_2, (player_B_location, 160 + j * 40))
    pygame.draw.line(screen, black, (0, 100), (x_length, 100), 3)
    pygame.draw.line(screen, black, (0, 100), (x_length, 100), 3)
    pygame.draw.line(screen, black, (0, 150), (x_length, 150), 3)
    pygame.draw.line(screen, gray, (0, 430), (x_length, 430), 3)
    pygame.draw.line(screen, gray, (0, 470), (x_length, 470), 3)
    pygame.draw.line(screen, gray, (0, 750), (x_length, 750), 3)
    pygame.draw.line(screen, black, (0, 790), (x_length, 790), 3)
    pygame.draw.line(screen, gray, (150, 100), (150, y_length), 3)
    pygame.draw.line(screen, gray, (375, 100), (375, y_length), 3)
    pygame.display.update()


#
# def draw_again():
#     for i in range(5):
#         screen.blit(img[dice[i]], (i * 100, 0))
#     score_now = count_score()
#     if player == 1:
#         location = player_A_location
#     else:
#         location = player_B_location
#     for j in range(17):
#         if score_record_1[j] != -1:
#             single_score_1 = font_small.render(str(score_now[j]), True, font_color)
#             screen.blit(single_score_1, (location, 160 + j * 40))
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
def select_dice(x):
    if roll_time < 3:
        if event.type == MOUSEBUTTONDOWN:
            (mouse_x, mouse_y) = pygame.mouse.get_pos()
            for i in range(5):
                if (mouse_x - (i * 100 + 50)) ^ 2 + (mouse_y - 50) ^ 2 < select_range ^ 2 and (
                        i + 1) not in x:
                    x.append(i + 1)
                if (mouse_x - (i * 100 + 50)) ^ 2 + (mouse_y - 50) ^ 2 < select_range ^ 2 and (i + 1) in selected_dice:
                    x.remove(i + 1)
                else:
                    pass


# 掷骰子
def roll_dice(event, selected_dice):
    if roll_time < 3:
        if event.type == MOUSEBUTTONDOWN:
            (mouse_x, mouse_y) = pygame.mouse.get_pos()
            if ((mouse_x - 544) ^ 2 + (mouse_y - 48) ^ 2) ^ 0.5 < select_range:
                for i in selected_dice:
                    dice[i] = random.randint(1, 6)
    selected_dice = []


while True:
    for event in pygame.event.get():
        selected_dice = []
        select_dice(selected_dice)
        roll_dice(event, selected_dice)

#
# def draw_dice():
#     for i in range(5):
#         screen.blit(img[dice[i]],(50, i*50))
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
#     screen.blit(textSurfaceObj, textRectObj)
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
