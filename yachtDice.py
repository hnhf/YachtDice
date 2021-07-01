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
screen = pygame.display.set_mode((600, 1000))
pygame.display.set_caption('游艇骰子')
pygame.init()

# 图片导入
img = [pygame.image.load('./images/1.png'), pygame.image.load('./images/2.png'), pygame.image.load('./images/3.png'),
       pygame.image.load('./images/4.png'), pygame.image.load('./images/5.png'), pygame.image.load('./images/6.png')]

# 颜色
white = (255, 255, 255)
gray = (200, 200, 200)

# 分数记录
dice = np.zeros(5)
score_now_1 = np.zeros(17)
score_now_2 = np.zeros(17)
score_record_1 = np.zeros(17)
score_record_2 = np.zeros(17)
list_1 = ['玩家', '1', '2', '3', '4', '5', '6', 'bonus', '上半', '三条', '四条', '葫芦', '小顺', '大顺', '游艇', '全计', '下半', '总分']

# 显示数字
font_size_big = 10
font_color = (0, 255, 255)
font_big = pygame.font.Font("resources/font/Gabriola.ttf", font_size_big)


def draw_board():
    for i in range(5):
        screen.blit(img[dice[i]], (i * 100 + 50, 50))
    roll_cha = font_big.render('摇', True, font_color)
    screen.blit(roll_cha, (550, 50))
    player_A = font_big.render('A', True, font_color)
    player_B = font_big.render('B', True, font_color)
    screen.blit(player_A, (300, 125))
    screen.blit(player_B, (500, 125))
    for j in range(18):
        element_1 = font_big.render(list_1[j], True, font_color)
        screen.blit(element_1, (100, 125 + j * 50))
    for k in range(17):
        single_score_1 = font_big.render(str(score_record_1[k]), True, font_color)
        single_score_2 = font_big.render(str(score_record_2[k]), True, font_color)
        screen.blit(single_score_1, (300, 175 + k * 50))
        screen.blit(single_score_2, (500, 175 + k * 50))
    pygame.display.update()


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
