"""
Author:weizhanfei
Created:2017/7/22
Purpose:
"""
import os.path as p
import file
import format_time
from lib import *

CRASH = "CRASH"
ANR = "ANR"
MONKEY_ABORTED = "monkey aborted"
NO_ACTIVITIES = "No activities"
OUT_OF_MEMORY = "Out of memory"
NULL_POINTER_EXCEPTION = "NullPointerException"
EXCEPTION = "Exception"
TIME_OUT = "TimedOut"
ERROR = "Error"
RUNTIME_EXCEPTION = "RuntimeException"
IO_EXCEPTION = "IOException "
ERROR_DICT = {CRASH: 0,
              MONKEY_ABORTED: 0,
              NO_ACTIVITIES: 0,
              ANR: 0,
              OUT_OF_MEMORY: 0,
              ERROR: 0,
              TIME_OUT: 0,
              NULL_POINTER_EXCEPTION: 0,
              RUNTIME_EXCEPTION: 0,
              IO_EXCEPTION: 0,
              EXCEPTION: 0
              }


# 将日志写入到文件

def write_log_to_txt(log_path, log):
    with open(log_path, "wt") as f:
        for l in log:
            f.write(l)
    f.close()


# 写Monkey报告的头部信息
def write_report_title(work_book, worksheet):
    title_format = work_book.add_format()
    title_format.set_center_across()
    title_format.set_font_size(20)
    title_format.set_bold()
    row = 0
    col = 0
    worksheet.write(row, col, "MonkeyReport", title_format)
    for i in range(len(ERROR_DICT) + 3):
        col += 1
        worksheet.write_blank(row, col, "", title_format)
    worksheet.write(1, 0, "手机品牌")
    worksheet.write(1, 1, "手机型号")
    worksheet.write(1, 2, "设备号")
    worksheet.write(1, 3, "测试包名")
    row = 1
    col = 3
    for i in ERROR_DICT.keys():
        col += 1
        worksheet.write(row, col, i)
    col += 1
    worksheet.write(row, col, "日志名")


# 写Monkey报告的主体信息
def write_report_body(work_book, worksheet, report_list):
    warring_format = work_book.add_format()
    warring_format.set_font_color('red')
    row = 1
    for report in report_list:
        col = 3
        row += 1
        worksheet.write(row, 0, report.phone_brand)
        worksheet.write(row, 1, report.phone_model)
        worksheet.write(row, 2, report.phone_device)
        worksheet.write(row, 3, report.phone_package)
        temp_dict = report.get_error_dict()
        for key in temp_dict.keys():
            col += 1
            if temp_dict[key] > 0:
                worksheet.write(row, col, temp_dict[key], warring_format)
            else:
                worksheet.write(row, col, temp_dict[key])
        col += 1
        worksheet.write_url(row, col, report.file_name)


# 写Monkey报告的尾部信息
def write_report_foot(work_book, worksheet, report_list, sum_error_dict):
    warring_format = work_book.add_format()
    warring_format.set_font_color('red')
    row = 2 + len(report_list)
    col = 3
    worksheet.write(row, 0, "合计")
    for key in sum_error_dict.keys():
        col += 1
        if sum_error_dict[key] > 0:
            worksheet.write(row, col, sum_error_dict[key], warring_format)
        else:
            worksheet.write(row, col, sum_error_dict[key])


# 获取Monkey报告
def get_report(log_path):
    sum_error_dict = ERROR_DICT.copy()
    report_name = log_path + p.sep + format_time.get_format_time('%Y%m%d%H%M%S') + "MonkeyReport.xlsx"
    workbook1 = xlsxwriter.Workbook(report_name)
    worksheet = workbook1.add_worksheet()
    write_report_title(workbook1, worksheet)

    log_list = file.get_all_file(log_path, filter_file="monkey.txt")
    report_list = []
    for log in log_list:
        report = Analysis(log)
        report_list.append(report)
        temp_dict = report.get_error_dict()
        for keys in temp_dict.keys():
            sum_error_dict[keys] += temp_dict[keys]
    write_report_body(workbook1, worksheet, report_list)
    write_report_foot(workbook1, worksheet, report_list, sum_error_dict)
    workbook1.close()


# 写性能报告的头部信息
def write_perf_summary_title(work_book, worksheet):
    title_format = work_book.add_format()
    title_format.set_center_across()
    title_format.set_font_size(20)
    title_format.set_bold()
    row = 0
    col = 0
    worksheet.write(row, col, "PerformanceSummary", title_format)
    for i in range(5):
        col += 1
        worksheet.write_blank(row, col, "", title_format)
    worksheet.write(1, 0, "设备号")
    worksheet.write(1, 1, "事务名")
    worksheet.write(1, 2, "响应时间")
    worksheet.write(1, 3, "下行流量")
    worksheet.write(1, 4, "上行流量")


# 写性能报告的主体信息
def write_perf_body_from_list(work_book, worksheet, temp_list, row=0, col=0):
    work_book.add_format()
    row_temp = row
    for temp in temp_list:
        col_temp = col
        for i in temp:
            worksheet.write(row_temp, col_temp, i)
            col_temp += 1
        row_temp += 1


# 获取性能报告
def get_perf_report(log_path, perf_summary_list, top_list, tcp_rcv_list, tcp_snd_list):
    report_name = log_path + p.sep + format_time.get_format_time('%Y%m%d%H%M%S') + "PerformanceReport.xlsx"
    workbook1 = xlsxwriter.Workbook(report_name)
    worksheet1 = workbook1.add_worksheet("Summary")
    worksheet2 = workbook1.add_worksheet("TOP")
    worksheet3 = workbook1.add_worksheet("流量下行")
    worksheet4 = workbook1.add_worksheet("流量上行")
    write_perf_summary_title(workbook1, worksheet1)
    write_perf_body_from_list(workbook1, worksheet1, perf_summary_list, 2, 0)
    write_perf_body_from_list(workbook1, worksheet2, top_list)
    write_perf_body_from_list(workbook1, worksheet3, tcp_rcv_list)
    write_perf_body_from_list(workbook1, worksheet4, tcp_snd_list)
    workbook1.close()
    pass


class Analysis:
    log_path = ""
    phone_device = "未知设备"
    phone_model = "未知型号"
    phone_brand = "未知品牌"
    phone_package = "未知包名"
    file_name = ""

    def __init__(self, log_path):
        self.log_path = log_path
        self.file_name = p.split(log_path)[-1]
        temp_list = self.file_name.split("+")
        if len(temp_list) > 3:
            self.phone_brand = temp_list[0]
            self.phone_model = temp_list[1]
            self.phone_device = temp_list[2]
            self.phone_package = temp_list[3]
        self.error_type_dict = self.get_error_dict()

    def get_error_dict(self):
        error_dict = ERROR_DICT.copy()
        with open(self.log_path, "r") as f:
            for line in f:
                for error_type in error_dict.keys():
                    if error_type in line:
                        error_dict[error_type] += 1
        f.close()
        return error_dict


if __name__ == '__main__':
    path = r"D:\monkeytest\20170722"
    get_report(path)
