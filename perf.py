"""
Author:weizhanfei
Created:2017/7/25
Purpose:
"""

import adb
import time
import config


def sum_range(num):
    for i in range(num):
        sum += i
    return sum


def get_perf(device, package):
    # 返回uid,cpu,vss,rss
    top = get_top_list(device, package)
    return top[1], top[4], top[7], top[8]


def get_top_list(device, package):
    top = adb.get_top(device, package)
    # report.write_log_to_txt("d:\\" + str(time.time()) + ".txt", top)
    return top.split()


# 转化百分号字符串到数字
def get_percent_str_to_int(str_percent):
    return int(str_percent.strip("%"))


# 计算CPU响应的时间,这里有个误差会列表最后cpu_num个纪录小于cpu_percent时会丢失，懒得改了
def get_cpu_response(cpu_list, cpu_percent, cpu_num, end_cpu_percent, end_num):
    temp_list = []
    max_num = cpu_num if cpu_num > end_num else end_num
    length = len(cpu_list) - max_num - 1
    # print("待查列表长度为" + str(length))
    loop_flag = True
    loop_break = False
    # print(cpu_list)
    if length > 2:
        for i in range(length):
            # print("列表序号" + str(i))
            # print(cpu_list[i])
            if loop_flag:
                temp_sum = 0
                # 如果判断程序运行并不稳定，因为收集时可能程序刚好处于SLEEP状态，可增加採集次數后使用
                # print("高于次数" + str(temp_sum))
                # print(cpu_list[i])
                if (cpu_list[i][5] is "S") and loop_flag:
                    # print("程序并沒有没有运行啊")
                    continue
                for num in range(cpu_num):
                    if get_percent_str_to_int(cpu_list[i + num][4]) >= cpu_percent:
                        temp_sum += 1
                    if temp_sum == cpu_num:
                        loop_flag = False
                        break
            # 判断结束的条件按CPU为0%更为合适，先试下再改
            if not loop_flag:
                temp_sum = 0
                for num in range(end_num):
                    if get_percent_str_to_int(cpu_list[i + num][4]) <= end_cpu_percent:
                        temp_sum += 1
                    if temp_sum == end_num:
                        loop_break = True
                        break
            if (not loop_flag) and (not loop_break):
                # print("满足条件:")
                # print("CPU使用率" + str(get_percent_str_to_int(cpu_list[i][4])))
                temp_list.append(cpu_list[i])
            if (not loop_flag) and loop_break:
                break
    # print(temp_list)
    if len(temp_list) >= 2:
        start_time = float(temp_list[0][13])
        end_time = float(temp_list[-1][13])
        return '%.2f' % (end_time - start_time)
    else:
        return "0.00"


# 根据TOP_LIST计算事务的响应时间


def get_transaction_response_time(top_list, device, transaction_name):
    temp_list = []
    for top in top_list:
        # print(top)
        if (device in top) and (transaction_name in top):
            # print("符合条件的")
            temp_list.append(top)
    return get_cpu_response(temp_list, config.cpu_percent, config.cpu_num,
                            config.end_cpu_percent, config.end_num)  # for i in range(len(top_list)):

    #       if (device, transaction_name in top_list[i]) and ("0%" not in top_list[i]):
    #           temp_list.append(top_list[i])


# 根据流量
def get_transaction_tcp(tcp_list, device, transaction_name):
    temp_list = []
    for tcp in tcp_list:
        if (device in tcp) and (transaction_name in tcp):
            temp_list.append(tcp)
    if temp_list.__len__() >= 2:
        return str(int(temp_list[-1][3]) - int(temp_list[0][3]))
    else:
        return "0"


def get_pss(device, package):
    meminfo = adb.get_meminfo(device, package).split()
    i = 0
    for mem in meminfo:
        i += 1
        if mem == "TOTAL":
            return meminfo[i]
    return ""


if __name__ == '__main__':
    now = lambda: time.time()
