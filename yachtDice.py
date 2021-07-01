# -*- coding: utf-8 -*-
"""
Created on Thu Jul  1 17:14:09 2021

@author: Fan
"""
import pygame
import sys
from pygame.locals import *
from collections import Counter
import socket
from socket import *
from time import ctime
import json
import select
#asdfafadf
#界面初始化
screen = pygame.display.set_mode((1000,500))
pygame.display.set_capyion('游艇骰子')
pygame.init()

#图片导入
img = []
img[0] = pygame.image.load('D:/Program/YachtDice/images/1.png')
img[1] = pygame.image.load('D:/Program/YachtDice/images/2.png')
img[2] = pygame.image.load('D:/Program/YachtDice/images/3.png')
img[3] = pygame.image.load('D:/Program/YachtDice/images/4.png')
img[4] = pygame.image.load('D:/Program/YachtDice/images/5.png')
img[5] = pygame.image.load('D:/Program/YachtDice/images/6.png')

#用于传递的数据
msg = []

#游戏界面定义
game_board = [[]]


#掷骰子
def roll_dice():
    if event.type == MOUSEBUTTONDOWN:
        pos_dice = pygame.mouse.get_pos()
        if pos_dice
        

def draw_dice():
    for i in range(6):
        screen.blit(img[dice[i]],(50, i*50))
    pygame.display.update()

#选择分数
def choose_score():
    if event.type == MOUSEBUTTONDOWN:
        pos_score = pygame.mouse.get_pos()


def game_over():
    if game_turn == 13:
        return 1
    else:
        return 0



#主循环
draw_board()
score_now_1 = []
score_now_2 = []
score_record_1 = []
score_record_2 = []

while True:
    rs,ws,es=select.select(inputs,[],[],0)
    for r in rs:
        if r is tcpCliSock:
            data,addr = r.recvfrom(BUFSIZE)
            draw_text('你的回合',200,420,15)
            data=json.loads(data)
            settable=1
            black_chess.append(data)
            bcx.append(data[0])
            bcy.append(data[1])
    for event in pygame.event.get():
        if event.type == QUIT:
            tcpCliSock.close()
            pygame.quit()
            sys.exit()
        if settable == 1:
            roll_time = 1
            roll_dice()
            if roll_time < 3:
                roll_time += 1
                roll_dice()
            else:
                if choose_score() = 1:
                    count_score
                    draw_text('对手回合', 200, 420, 15)
                    settable = 0
                    msg1 = json.dumps(msg)
                    ACTIVEEVENTtcpCliSock.sendto(msg1.encode(), ADDR)
                    msg = []
    draw_dice()
    if gameover() == 1:
        draw_text('你赢了！', 200, 420, 15)
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
    elif gameover() == 2:
        draw_text('你输了！', 200, 420, 15)
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
    elif gameover() == 3:
        draw_text('平局！', 200, 420, 15)
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()



    