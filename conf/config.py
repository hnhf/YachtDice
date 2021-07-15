# 其他参数
select_range = 30  # 鼠标点击的有效半径
player_number = 2  # 玩家数量

# 界面初始化
dice_length = 100
roll_length = 100
list_y_length = 36
list_x_length = 200
x_length = dice_length * 5 + roll_length
y_length = dice_length + list_y_length * 18
list_player_length = (x_length - list_x_length)

# 字体大小和位置
roll_font = 58
score_font = 20
roll_position = (dice_length * 5 + roll_length / 2 - roll_font / 2, roll_length / 2 - roll_font / 2 - roll_length / 10)
roll_circle_position = (dice_length * 5 + roll_length / 2, roll_length / 2 - roll_length / 10)
roll_circle_radius = 30
player_location2 = [list_x_length + (x_length - list_x_length) / 4, list_x_length + (x_length - list_x_length) * 3 / 4]
player_location3 = [list_x_length + (x_length - list_x_length) / 6, list_x_length + (x_length - list_x_length) / 2,
                    list_x_length + (x_length - list_x_length) * 5 / 6]
locations = [player_location2, player_location3]

# 颜色
black = (0, 0, 0)
white = (255, 255, 255)
gray = (150, 150, 150)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
cyan = (0, 255, 255)
purple = (255, 0, 255)

player_1_location = list_x_length + list_player_length / 2
player_2_location = list_x_length + list_player_length * 1.5
score_list = ['一点', '二点', '三点', '四点', '五点', '六点', '奖励', '上半区', '三条', '四条',
              '葫芦', '小顺', '大顺', '游艇', '全计', '下半区', '总分']
