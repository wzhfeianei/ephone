"""
Author:weizhanfei
Created:2017/7/22
Purpose:
"""
import configparser

import format_time

cp = configparser.ConfigParser()
cp.read('config.conf')
# Monkey设置
packages = cp.get("app", "packages").split(",")
today = format_time.get_format_time("%Y%m%d")
default_entry_event_num = cp.get("monkey", "default_entry_event_num")
default_entry_event_time_sep = cp.get("monkey", "default_entry_event_time_sep")
throttle = cp.get("monkey", "throttle")
touch = cp.get("monkey", "touch")
majornav = cp.get("monkey", "majornav")
syskeys = cp.get("monkey", "syskeys")
motion = cp.get("monkey", "motion")
appswitch = cp.get("monkey", "appswitch")
flip = cp.get("monkey", "flip")

# 默认的日志生成路径
default_entry_event_path = cp.get("monkey", "default_entry_event_path")
# 执行Monkey期间每隔多少秒记录一次性能
monkey_perf_time_sep = cp.get("monkey", "monkey_perf_time_sep")
# 报告生成的默认路径为当天日期的文件夹，填写"mytest"实际会在"D:\\monkeytest\\mytest"目录下生成
report_path = today

# 性能测试
package = cp.get("performance", "package")
perf_timeout = int(cp.get("performance", "perf_timeout"))
# 性能测试中统计事务时敏感度，当CPU使用率大于cpu_percent的次数多于cpu_num开始统计事务时间，
# 当CPU使用率为end_cpu_percent的次数大于end_num结束事务
cpu_percent = int(cp.get("performance", "cpu_percent"))
cpu_num = int(cp.get("performance", "cpu_num"))
end_cpu_percent = int(cp.get("performance", "end_cpu_percent"))
end_num = int(cp.get("performance", "end_num"))


def config_set(config_path, section, option, value):
    config = configparser.ConfigParser()
    config.read(config_path)
    config.set(section, option, value)
    with open(config_path, "w") as f:
        config.write(f)
    f.close()


if __name__ == '__main__':
    print(packages)
    print(today)
    print(default_entry_event_num)
    print(default_entry_event_time_sep)
    print(default_entry_event_path)
    print(package)
    print(perf_timeout)
    print(cpu_percent)
    print(cpu_num)
    print(end_cpu_percent)
    print(end_num)
    print("majornav"+majornav)
    config_set("config.conf", "performance", "end_num", "5")
