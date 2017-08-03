"""
Author:weizhanfei
Created:2017/7/22
Purpose:
"""
import time


def get_format_time(format_string):
    return time.strftime(format_string, time.localtime(time.time()))
