"""
Author:weizhanfei
Created:2017/7/28
Purpose:
"""
import time
import threading
import adb


def del_per(str):
    return int(str.strip("%"))


class Transaction:
    def __init__(self, transaction_name, top_list):
        pass


if __name__ == '__main__':
    t = Transaction("dfasdf", "dfadsfa", "dfadsf")
    t.start()
    time.sleep(3)
    t.end()
