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


if __name__ == "__main__":
    y = Ytz("seed")
    y.run()
