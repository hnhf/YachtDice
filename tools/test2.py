# -*- coding: utf-8 -*-
"""
Created on Thu Jul  1 17:14:09 2021
@author: Fan
"""
from yachtDice import Ytz
from threading import Thread


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
