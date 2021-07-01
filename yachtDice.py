# -*- coding: utf-8 -*-
"""
Created on Thu Jul  1 17:14:09 2021

@author: Fan
"""
import pygame
import sys
import numpy as np
from pygame.locals import *
from collections import Counter
from time import ctime
import json

# 界面初始化
screen = pygame.display.set_mode((600, 820))
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

# 分数记录
dice = [1, 2, 3, 4, 5]
score_now_1 = np.zeros(17, dtype=int)
score_now_2 = np.zeros(17,dtype=int)
score_record_1 = np.zeros(17,dtype=int)
score_record_2 = np.zeros(17,dtype=int)
list_1 = ['1点', '2点', '3点', '4点', '5点', '6点', 'Bonus', '上半区总分', '三条', '四条',
          '葫芦', '小顺','大顺', '游艇', '全计', '下半区总分', '总分']

# 显示数字
font_color = (0, 0, 0)
font_small = pygame.font.Font('C:/Windows/Fonts/simhei.ttf', 16)
font_middle = pygame.font.Font('C:/Windows/Fonts/simhei.ttf', 28)
font_big = pygame.font.Font('C:/Windows/Fonts/simhei.ttf', 65)


def draw_board():
    screen.fill(bg_color)
    for i in range(5):
        screen.blit(img[dice[i]], (i * 100, 0))
    roll_cha = font_big.render('摇', True, red)
    screen.blit(roll_cha, (510, 15))
    players = font_middle.render('玩家', True, font_color)
    player_A = font_middle.render('A', True, font_color)
    player_B = font_middle.render('B', True, font_color)
    screen.blit(players, (35, 110))
    screen.blit(player_A, (248, 110))
    screen.blit(player_B, (473, 110))
    for j in range(17):
        element_1 = font_small.render(list_1[j], True, font_color)
        screen.blit(element_1, (50, 160 + j * 40))
        single_score_1 = font_small.render(str(score_record_1[j]), True, font_color)
        single_score_2 = font_small.render(str(score_record_2[j]), True, font_color)
        screen.blit(single_score_1, (250, 160 + j * 40))
        screen.blit(single_score_2, (475, 160 + j * 40))
    pygame.draw.line(screen, black, (0, 100), (600, 100), (3))
    pygame.draw.line(screen, black, (0, 100), (600, 100), (3))
    pygame.draw.line(screen, black, (0, 150), (600, 150), (3))
    pygame.draw.line(screen, gray, (0, 430), (600, 430), (3))
    pygame.draw.line(screen, gray, (0, 470), (600, 470), (3))
    pygame.draw.line(screen, gray, (0, 750), (600, 750), (3))
    pygame.draw.line(screen, black, (0, 790), (600, 790), (3))
    pygame.draw.line(screen, gray, (150, 100), (150, 820), (3))
    pygame.draw.line(screen, gray, (375, 100), (375, 820), (3))
    pygame.display.update()

while True:
    draw_board()

# #掷骰子
# def roll_dice():
#     if event.type == MOUSEBUTTONDOWN:
#         pos_dice = pygame.mouse.get_pos()
#         if pos_dice
#
#
# def draw_dice():
#     for i in range(5):
#         screen.blit(img[dice[i]],(50, i*50))
#     pygame.display.update()
#
# #选择分数
# def choose_score():
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
