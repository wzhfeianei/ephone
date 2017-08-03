"""
Author:weizhanfei
Created:2017/8/1
Purpose:
"""
from tkinter import *


class TransactionText:
    def __init__(self, parent):
        self.device_text = Text(parent, width=20, height=42)
        self.name_text = Text(parent, width=30, height=42)
        self.time_text = Text(parent, width=10, height=42)
        self.tcp_rev_text = Text(parent, width=10, height=42)
        self.tcp_snd_text = Text(parent, width=10, height=42)
        self.device_text.insert(INSERT, "       设备号\n")
        self.name_text.insert(INSERT, "             事务名\n")
        self.time_text.insert(INSERT, " 响应时间\n")
        self.tcp_rev_text.insert(INSERT, " 接收流量\n")
        self.tcp_snd_text.insert(INSERT, " 发送流量\n")
        self.text_list = [self.device_text, self.name_text, self.time_text, self.tcp_rev_text, self.tcp_snd_text]

    def apply(self):
        i = 0
        for t in self.text_list:
            t.grid(row=0, column=i)
            i += 1
            # self.device_text.grid(row=0, column=0)
            # self.name_text.grid(row=0, column=1)
            # self.time_text.grid(row=0, column=2)
            # self.tcp_rev_text.grid(row=0, column=3)
            # self.tcp_snd_text.grid(row=0, column=4)

    def grid_forget(self):
        i = 0
        for t in self.text_list:
            # t.delete(1.0, END)
            t.grid_forget()
            i += 1
            # self.device_text.delete(0.0, END)
            # self.name_text.delete(0.0, END)
            # self.time_text.delete(0.0, END)
            # self.tcp_rev_text.delete(0.0, END)
            # self.tcp_snd_text.delete(0.0, END)

            # self.device_text.grid_forget()
            # self.name_text.grid_forget()
            # self.time_text.grid_forget()
            # self.tcp_rev_text.grid_forget()
            # self.tcp_snd_text.grid_forget()

    def insert_perf(self, perf_list):
        i = 0
        for t in self.text_list:
            if len(perf_list[i]) > t['width']:
                print("宽度超出了")
                for m in range(len(perf_list)):
                    if m is not i:
                        perf_list[m] += "\n"
            i += 1
        self.device_text.insert(INSERT, perf_list[0] + "\n")
        self.name_text.insert(INSERT, perf_list[1] + "\n")
        self.time_text.insert(INSERT, " " + perf_list[2] + "\n")
        self.tcp_rev_text.insert(INSERT, perf_list[3] + "\n")
        self.tcp_snd_text.insert(INSERT, perf_list[4] + "\n")

    def delete_data(self):
        i = 0
        for t in self.text_list:
            t.delete(2.0, END)
            t.insert(INSERT, "\n")
            i += 1
