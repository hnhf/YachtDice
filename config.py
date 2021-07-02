import numpy as np

# 界面初始化
x_length = 600
y_length = 820

# 颜色
white = (255, 255, 255)
gray = (200, 200, 200)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
black = (0, 0, 0)

# 其他参数
select_range = 30  # 鼠标点击的有效半径
player_number = 2  # 玩家数量
player_A_location = 250
player_B_location = 475
score_list = ['1点', '2点', '3点', '4点', '5点', '6点', 'Bonus', '上半区总分', '三条', '四条',
              '葫芦', '小顺', '大顺', '游艇', '全计', '下半区总分', '总分']
