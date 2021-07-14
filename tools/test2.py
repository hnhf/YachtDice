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
from yachtDice import Ytz
from threading import Thread

pygame.display.set_caption('游艇骰子')
pygame.init()
font_roll = pygame.font.Font(get_path('resource/font/simhei.ttf'), config.roll_font)
font_score = pygame.font.Font(get_path('resource/font/simhei.ttf'), 20)
font_player = pygame.font.Font(get_path('resource/font/simhei.ttf'), 28)
font_20 = pygame.font.Font(get_path('resource/font/simhei.ttf'), 20)
font_25 = pygame.font.Font(get_path('resource/font/simhei.ttf'), 25)
font_30 = pygame.font.Font(get_path('resource/font/simhei.ttf'), 30)
IP = '192.168.31.8'
PORT = 6666
# 建立socket连接
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP, PORT))


def main():
    # logger.info("请输入昵称:")
    # p_name = input()
    # logger.info("请输入玩家数量:")
    # p_number = input()
    p_name = 'xiaopang'
    p_number = '3'
    y = Ytz(p_name, p_number)
    threads = list()
    threads.append(Thread(target=y.send_data))
    threads.append(Thread(target=y.recv_data))
    for thread in threads:
        thread.start()


if __name__ == "__main__":
    main()
