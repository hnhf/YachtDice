import numpy as np

# 界面初始化
x_length = 600
y_length = 820
bg_color = (255, 255, 255)

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

score_list = ['1点', '2点', '3点', '4点', '5点', '6点', 'Bonus', '上半区总分', '三条', '四条',
              '葫芦', '小顺', '大顺', '游艇', '全计', '下半区总分', '总分']
