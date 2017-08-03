"""
Author:weizhanfei
Created:2017/7/22
Purpose:
"""
from devices import *
from report import *
import format_time
import os.path as p
import os
import file
import time
import threading

adb = "adb"
adb_devices = "adb devices"
adb_s = "adb -s"
top_list = []
tcp_rcv_list = []
tcp_snd_list = []


def execute(command):
    return os.popen(command).readlines()


def execute_read(command):
    return os.popen(command).read()


# 获取设备列表
def get_devices():
    devices = execute('adb devices')
    devices.pop()
    devices.pop(0)
    devices_list = []
    for i in devices:
        devices_list.append(i.replace("\tdevice\n", ""))
    return devices_list


# 获取top
def get_top(device, package, transaction_name=""):
    command = "adb -s %s shell top -n 1 |findstr %s" % (device, package)
    # print("事务名："+transaction_name)
    for top in execute(command):
        if not package + ":" in top:
            if top is None:
                temp_list = ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                             '']
            else:
                temp_list = top.split()
            temp_list.append(device)
            temp_list.append(transaction_name)
            temp_list.append(str(time.time()))
            top_list.append(temp_list)
        if len(temp_list) < 1:
            raise ValueError
        return temp_list


# 根据PID获取UID
def get_uid(device, pid):
    command = "adb -s %s shell cat /proc/%s/status |findstr Uid" % (device, pid)
    for res in execute(command):
        if "Uid" in res:
            return res.split()[1]
    return ""


# 获取接收流量
def get_tcp_rcv(device, package, transaction_name=""):
    pid = get_top(device, package)[0]
    # print("pid is "+pid)
    uid = get_uid(device, pid)
    # print("uid is " + uid)
    command = "adb -s %s shell cat /proc/uid_stat/%s/tcp_rcv" % (device, uid)
    temp_list = [device, package, transaction_name]
    for res in execute(command):
        # print("查看流量成功")
        if len(res) > 0:
            temp_list.append(res.split()[0])
            tcp_rcv_list.append(temp_list)
            return res.split()[0]
    temp_list.append("0")
    tcp_rcv_list.append(temp_list)
    return "0"


# 获取发送流量
def get_tcp_snd(device, package, transaction_name=""):
    pid = get_top(device, package)[0]
    uid = get_uid(device, pid)

    command = "adb -s %s shell cat /proc/uid_stat/%s/tcp_snd" % (device, uid)
    temp_list = [device, package, transaction_name]
    for res in execute(command):
        if len(res) > 0:
            temp_list.append(res.split()[0])
            tcp_snd_list.append(temp_list)
            return res.split()[0]
    temp_list.append("0")
    tcp_snd_list.append(temp_list)
    return "0"


# 获取流量
def get_tcp(device, package, transaction_name=""):
    # print(device, package)
    # tcp_rcv = get_tcp_rcv(device, package)
    # tcp_snd = get_tcp_snd(device, package)
    threading.Thread(target=get_tcp_rcv, args=(device, package, transaction_name)).start()
    threading.Thread(target=get_tcp_snd, args=(device, package, transaction_name)).start()
    # return tcp_rcv, tcp_snd


# 阻塞上下文的获取流量
def get_tcp_join(device, package, transaction_name=""):
    # print(device, package)
    # tcp_rcv = get_tcp_rcv(device, package)
    # tcp_snd = get_tcp_snd(device, package)
    threads = [threading.Thread(target=get_tcp_rcv, args=(device, package, transaction_name)),
               threading.Thread(target=get_tcp_snd, args=(device, package, transaction_name))]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
        # return tcp_rcv, tcp_snd


# 获取一个固定时间内的top列表
def get_long_top(device, package, num, transaction_name):
    # print("啦啦啦"+transaction_name)
    threads = []
    for i in range(num * 20):
        threads.append(threading.Thread(target=get_top, args=(device, package, transaction_name)))
        threads[-1].start()
        time.sleep(0.05)


# 获取内存
def get_meminfo(device, package):
    command = "adb -s %s shell dumpsys meminfo  %s" % (device, package)
    meminfo = execute_read(command)
    if "error" not in meminfo:
        return meminfo
    else:
        return ""


# 执行Monkey并记录执行结果
def get_monkey(devices_path, phone, packages, monkey_num, throttle, touch, majornav, syskeys, motion, appswitch, flip,
               anyevent):
    for i in packages:
        event_sum = int(touch) + int(majornav) + int(syskeys) + int(motion) + int(appswitch) + int(flip)
        if event_sum == 0:
            command = "adb -s  %s shell monkey -p  %s --throttle %s " \
                      "--ignore-crashes --ignore-timeouts --ignore-security-exceptions " \
                      "--ignore-native-crashes  --monitor-native-crashes --wait-dbg -v -v -v %s" \
                      % (phone.device, i, throttle, monkey_num)
        else:
            command = "adb -s  %s shell monkey -p  %s  " \
                      "--throttle %s --pct-touch %s --pct-majornav %s --pct-syskeys %s --pct-motion %s " \
                      "--pct-appswitch %s --pct-flip %s --pct-anyevent %s " \
                      "--ignore-crashes --ignore-timeouts --ignore-security-exceptions " \
                      "--ignore-native-crashes  --monitor-native-crashes --wait-dbg -v -v -v %s" \
                      % (phone.device, i, throttle, touch, majornav, syskeys, motion, appswitch, flip, anyevent,
                         monkey_num)
        # print(command)
        log = execute(command)
        log_name = devices_path + p.sep + phone.full_name + "+" + i + "+" + format_time.get_format_time(
            '%Y%m%d%H%M%S') + "monkey.txt"
        write_log_to_txt(log_name, log)  # 执行Monkey并记录TOP性能


def get_monkey_perf(log_path, phone, packages, time_sep):
    file.create_dir(log_path)
    time_flag = format_time.get_format_time('%Y%m%d%H%M%S')
    while True:
        for i in packages:
            try:
                log = get_top(phone.device, i)
                temp_log = []
                for element in log:
                    temp_log.append(element + "\t")
                temp_log.append("\n")
                print(temp_log)
                log_name = log_path + p.sep + phone.full_name + "+" + i + "+" + time_flag + "perf.txt"
                write_log_to_txt(log_name, temp_log)
            except ValueError as e:
                print("没有这个包")
        time.sleep(time_sep)


if __name__ == '__main__':
    # top
    # print(execute("adb -s GSLDU16716015230 shell top -n 1 |findstr com.hele.buyer"))
    # print(execute("adb shell dumpsys gfxinfo com.hele.buyer"))
    # ("GSLDU16716015230", "com.hele.buyer", 20, "fdasf")
    # print(get_tcp_snd("GSLDU16716015230", "com.hele.buyer"))
    # print(get_tcp_rcv("GSLDU16716015230", "com.hele.buyer"))
    print(get_top("GSLDU16716015230", "com.hele.1"))
