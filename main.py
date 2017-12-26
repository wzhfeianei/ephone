"""
Author:weizhanfei
Created:2017/7/22
Purpose:
"""
from devices import *
from adb import *
from report import *
from perf import *
from transaction_gui import *
from tkinter import messagebox
from tkinter import *
import format_time
import threading
import file
import os.path as p
import config


def init_list():
    temp_list = get_devices()
    list_box_device = []
    for device in temp_list:
        phone = Devices(device)
        list_box_device.append(phone.full_name)
    return list_box_device


if __name__ == '__main__':

    root = Tk()
    root.title("EA手机APP测试")

    frame_left_top = Frame(bg='white')
    frame_left_center = Frame(bg='white')
    frame_left_bottom = Frame(bg='white')
    frame_right = Frame(bg='white')
    # 添加环境变量
    sys.path.append(p.join(p.abspath("."), "lib"))
    # 设置容器位置
    frame_left_top.grid(row=0, column=0, padx=2, pady=2)
    frame_left_center.grid(row=1, column=0, padx=2, pady=2)
    frame_left_bottom.grid(row=2, column=0, padx=2, pady=2)
    frame_right.grid(row=0, column=1, rowspan=3, padx=2, pady=2)

    list1 = StringVar()
    list1.set(init_list())

    perf_summary_list = []


    def refresh_list():
        list1.set(init_list())


    def show_msg(*args):
        pass
        # indexs = listbox_left.curselection()
        # print(devices_list[indexs.index(0)])


    # 设备列表
    frame_left_top_labelframe = LabelFrame(frame_left_top, text="选中要测试设备(默认全选）")
    frame_left_top_labelframe.grid(row=0, column=0, padx=1, pady=1)
    scrollbar_left = Scrollbar(frame_left_top_labelframe)
    scrollbar_left.grid(row=0, column=1, padx=2, pady=2, sticky='ns')
    listbox_left = Listbox(frame_left_top_labelframe, width=56, height=11, listvariable=list1,
                           yscrollcommand=scrollbar_left.set,
                           selectmode=EXTENDED)
    listbox_left.grid(row=0, column=0, padx=2, pady=2, sticky='ns')
    scrollbar_left.config(command=listbox_left.yview)
    button_left = Button(frame_left_top_labelframe, text="刷新列表", command=refresh_list)
    button_left.grid(row=1, column=0)

    listbox_left.bind("<<ListboxSelect>>", show_msg)

    # Monkey 参数设置
    frame_left_center_labelframe = LabelFrame(frame_left_center, text="Monkey设置")
    frame_left_center_labelframe.grid(row=1, column=0, padx=2, pady=2)

    # 默认值
    # 事件数量
    default_entry_event_num = StringVar()
    default_entry_event_num.set(config.default_entry_event_num)

    # 日志路径
    default_entry_event_path = StringVar()
    default_entry_event_path.set(config.default_entry_event_path)
    file.create_dir(default_entry_event_path.get())

    # 性能记录类型
    perf_type = StringVar()
    perf_type.set("trans")

    # Monkey触摸事件百分比
    monkey_touch_percent = StringVar()
    monkey_touch_percent.set(config.touch)
    Label(frame_left_center_labelframe, text=' 触摸事件百分比:    ').grid(row=0, column=0)
    Entry(frame_left_center_labelframe, width=6, textvariable=monkey_touch_percent).grid(row=0, column=1)

    # Monkey导航事件百分比
    monkey_banner_percent = StringVar()
    monkey_banner_percent.set(config.majornav)
    Label(frame_left_center_labelframe, text=' 导航事件百分比:    ').grid(row=1, column=0)
    Entry(frame_left_center_labelframe, width=6, textvariable=monkey_banner_percent).grid(row=1, column=1)

    # Monkey系统按键百分比
    monkey_system_percent = StringVar()
    monkey_system_percent.set(config.syskeys)
    Label(frame_left_center_labelframe, text=' 系统按键百分比:    ').grid(row=2, column=0)
    Entry(frame_left_center_labelframe, width=6, textvariable=monkey_system_percent).grid(row=2, column=1)

    # Monkey滑动事件百分比
    monkey_slide_percent = StringVar()
    monkey_slide_percent.set(config.motion)
    Label(frame_left_center_labelframe, text=' 滑动事件百分比:    ').grid(row=3, column=0)
    Entry(frame_left_center_labelframe, width=6, textvariable=monkey_slide_percent).grid(row=3, column=1)

    # Monkey activity之间的切换百分比
    monkey_activity_percent = StringVar()
    monkey_activity_percent.set(config.appswitch)
    Label(frame_left_center_labelframe, text=' 组件切换百分比:    ').grid(row=4, column=0)
    Entry(frame_left_center_labelframe, width=6, textvariable=monkey_activity_percent).grid(row=4, column=1)

    # Monkey键盘事件
    monkey_flip_percent = StringVar()
    monkey_flip_percent.set(config.flip)
    Label(frame_left_center_labelframe, text=' 键盘事件百分比:    ').grid(row=5, column=0)
    Entry(frame_left_center_labelframe, width=6, textvariable=monkey_flip_percent).grid(row=5, column=1)

    # Monkey事件的数量
    Label(frame_left_center_labelframe, text='      事件数量:').grid(row=0, column=2)
    Entry(frame_left_center_labelframe, textvariable=default_entry_event_num).grid(row=0, column=3)
    Label(frame_left_center_labelframe, text='        ').grid(row=0, column=4)
    # Monkey事件间隔
    # 时间间隔
    default_entry_event_time_sep = StringVar()
    default_entry_event_time_sep.set(config.default_entry_event_time_sep)
    Label(frame_left_center_labelframe, text='      事件间隔:').grid(row=1, column=2)
    Entry(frame_left_center_labelframe, textvariable=default_entry_event_time_sep).grid(row=1, column=3)
    Label(frame_left_center_labelframe, text='        ').grid(row=1, column=4)

    # 日志所存放的路径
    Label(frame_left_center_labelframe, text='      日志路径:').grid(row=2, column=2)
    Entry(frame_left_center_labelframe, textvariable=default_entry_event_path).grid(row=2, column=3)


    def write_monkey_config():
        throttle = default_entry_event_time_sep.get()
        touch = monkey_touch_percent.get()
        majornav = monkey_banner_percent.get()
        syskeys = monkey_system_percent.get()
        motion = monkey_slide_percent.get()
        appswitch = monkey_activity_percent.get()
        flip = monkey_flip_percent.get()
        monkey_num = default_entry_event_num.get()
        log_path = default_entry_event_path.get()
        config_path = "config.conf"
        config.config_set(config_path, "monkey", "throttle", throttle)
        config.config_set(config_path, "monkey", "touch", touch)
        config.config_set(config_path, "monkey", "majornav", majornav)
        config.config_set(config_path, "monkey", "syskeys", syskeys)
        config.config_set(config_path, "monkey", "motion", motion)
        config.config_set(config_path, "monkey", "appswitch", appswitch)
        config.config_set(config_path, "monkey", "flip", flip)
        config.config_set(config_path, "monkey", "default_entry_event_num", monkey_num)
        config.config_set(config_path, "monkey", "default_entry_event_path", log_path)


    def set_monkey():
        # Monkey设置
        packages = config.packages
        devices_var = list1.get()
        devices_path = default_entry_event_path.get() + p.sep + format_time.get_format_time("%Y%m%d")
        file.create_dir(devices_path)
        devices_list = Devices.get_device_from_var(devices_var)
        if len(devices_list) < 1:
            messagebox.showerror('警告', '必须有手机连接ADB')
            return
        throttle = default_entry_event_time_sep.get()
        touch = monkey_touch_percent.get()
        majornav = monkey_banner_percent.get()
        syskeys = monkey_system_percent.get()
        motion = monkey_slide_percent.get()
        appswitch = monkey_activity_percent.get()
        flip = monkey_flip_percent.get()
        event_sum = int(touch) + int(majornav) + int(syskeys) + int(motion) + int(appswitch) + int(flip)
        monkey_num = default_entry_event_num.get()
        if event_sum > 100:
            messagebox.showerror('错误', '所有的事件的比例和不能超过100')
            return
        else:
            anyevent = str(100 - event_sum)

        if int(monkey_num) < 1:
            messagebox.showerror('错误', '运行次数至少为1次')
            return

        threads = []
        for device in devices_list:
            phone = Devices(device)
            threads.append(threading.Thread(target=get_monkey, args=(devices_path, phone, packages, monkey_num,
                                                                     throttle, touch, majornav, syskeys, motion,
                                                                     appswitch,
                                                                     flip, anyevent)))
            threads[-1].start()
            if perf_type.get() in "monkey":
                threads.append(threading.Thread(target=get_monkey_perf,
                                                args=(devices_path, phone, packages, config.monkey_perf_time_sep)))
                threads[-1].start()
        write_monkey_config()
        return


    # 获取Monkey报告
    def report():
        temp_path = default_entry_event_path.get() + p.sep + config.report_path
        file.create_dir(temp_path)
        get_report(temp_path)


    Label(frame_left_center_labelframe, text='      记录性能').grid(row=3, column=2)
    Radiobutton(frame_left_center_labelframe, variable=perf_type,
                value='monkey', ).grid(row=3, column=3, sticky=W)

    Button(frame_left_center_labelframe, text="启动Monkey", font=("黑体", 11, "bold"), command=set_monkey). \
        grid(row=4, column=3, columnspan=2, sticky=E)
    Button(frame_left_center_labelframe, text=" 生成报告 ", font=("黑体", 11, "bold"), command=report). \
        grid(row=5, column=3, columnspan=2, sticky=E)

    # 性能测试选项

    frame_left_bottom_labelframe = LabelFrame(frame_left_bottom, text="性能测试")
    frame_left_bottom_labelframe.grid(row=0, column=0, padx=2, pady=2)

    Label(frame_left_bottom_labelframe, text='  事务名:').grid(row=0, column=0)

    transaction_name_var = StringVar()

    entry_transaction_name = Entry(frame_left_bottom_labelframe, width=33, textvariable=transaction_name_var)
    entry_transaction_name.grid(row=0, column=1)

    # 性能测试包

    text_perf = TransactionText(frame_right)
    text_perf.apply()
    package = config.package


    def start_transaction():
        devices_var = list1.get()
        devices_list = Devices.get_device_from_var(devices_var)
        if len(devices_list) < 1:
            messagebox.showerror('警告', '必须有手机连接ADB')
            return
        transaction_name = transaction_name_var.get()
        if transaction_name is "":
            # print("事务名不能为空")
            messagebox.showerror('警告', '事务名不能为空')
            return
        # text.pack_forget()

        start_tran_button.config(state=DISABLED)
        entry_transaction_name.config(state=DISABLED)
        end_tran_button.config(state=ACTIVE)
        perf_top_threads = []
        for device in devices_list:
            perf_top_threads.append(
                threading.Thread(target=get_long_top, args=(device, package, config.perf_timeout, transaction_name)))
            perf_top_threads[-1].start()
            perf_top_threads.append(
                threading.Thread(target=get_tcp, args=(device, package, transaction_name)))
            perf_top_threads[-1].start()


    def end_transaction():
        devices_var = list1.get()
        devices_list = Devices.get_device_from_var(devices_var)
        # text.pack_info()
        transaction_name = transaction_name_var.get()
        start_tran_button.config(state=ACTIVE)
        # end_tran_button.config(state=DISABLED)
        entry_transaction_name.config(state=NORMAL)
        transaction_name_var.set("")
        # print(top_list)
        threads = []
        for device in devices_list:
            threads.append(threading.Thread(target=get_tcp_join, args=(device, package, transaction_name)))
            threads[-1].start()
        for t in threads:
            t.join()
        for device in devices_list:
            t = get_transaction_response_time(top_list, device, transaction_name)
            tran_tcp_snd = get_transaction_tcp(tcp_snd_list, device, transaction_name)
            tran_tcp_rcv = get_transaction_tcp(tcp_rcv_list, device, transaction_name)
            # print(transaction_name, t)
            temp_list = [device, transaction_name, t, tran_tcp_rcv, tran_tcp_snd]
            perf_summary_list.append(temp_list)
            text_perf.insert_perf(temp_list)


    start_tran_button = Button(frame_left_bottom_labelframe, text="开始事务", command=start_transaction)
    start_tran_button.grid(row=0, column=2)
    Label(frame_left_bottom_labelframe, text="  ").grid(row=1, column=3)
    end_tran_button = Button(frame_left_bottom_labelframe, text="结束事务", command=end_transaction)
    end_tran_button.config(state=DISABLED)
    end_tran_button.grid(row=0, column=4)


    def clear_text():
        top_list.clear()
        tcp_rcv_list.clear()
        tcp_snd_list.clear()
        text_perf.delete_data()
        # ext_perf.grid_forget()
        # 原输出框，暂时不用
        # text.pack()


    def perf_report():
        temp_path = default_entry_event_path.get() + p.sep + config.report_path
        file.create_dir(temp_path)
        get_perf_report(temp_path, perf_summary_list, top_list, tcp_rcv_list, tcp_snd_list)
        # print(perf_summary_list)
        # print(tcp_rcv_list)
        # print(tcp_snd_list)


    # 原输出框，暂时不用
    # text = Text(frame_right, width=60, height=33)
    # text.pack()
    Label(frame_left_bottom_labelframe, text="").grid(row=1, column=0)
    button_perf_clear = Button(frame_left_bottom_labelframe, text="清空纪录", command=clear_text)
    button_perf_clear.grid(row=2, column=2)

    Label(frame_left_bottom_labelframe, text="  ").grid(row=1, column=3)
    button_perf_report = Button(frame_left_bottom_labelframe, text="性能报告", command=perf_report)
    button_perf_report.grid(row=2, column=4)

    root.mainloop()
