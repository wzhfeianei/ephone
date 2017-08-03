"""
Author:weizhanfei
Created:2017/7/22
Purpose:
"""
from adb import *


class Devices:
    device = "未知设备"
    model = "未知型号"
    brand = "未知品牌"
    full_name = brand + "+" + model + "+" + device

    def __init__(self, devices):
        self.device = devices
        self.model = self.get_model()
        self.brand = self.get_brand()
        self.full_name = self.brand + "+" + self.model + "+" + self.device

    def get_model(self):
        command = "adb -s " + self.device + ' shell cat /system/build.prop | find "ro.product.model="'
        rt = execute(command)
        if len(rt) > 0:
            return rt[0][17:].strip("\r\n")
        else:
            return "未知型号"

    def get_brand(self):
        command = "adb -s " + self.device + ' shell cat /system/build.prop | find "ro.product.brand="'
        rt = execute(command)
        if len(rt) > 0:
            return rt[0][17:].strip("\r\n")
        else:
            return "未知品牌"

    @staticmethod
    def get_device_from_full_name(fullname):
        return fullname.split("+")[2]

    @staticmethod
    def get_device_from_var(var):
        temp_list = []
        for i in var.split("'"):
            if "+" in i:
                num = i.rfind("+") + 1
                temp_list.append(i[num:])
        return temp_list


if __name__ == '__main__':
    print(Devices.get_device_from_full_name("dafsd+ssfsd+df"))
