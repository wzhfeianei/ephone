"""
Author:weizhanfei
Created:2017/7/22
Purpose:
"""
from lib import *


def create_new_xlsx(file_path):
    # worksheet = workbook.add_worksheet()
    return xlsxwriter.Workbook(file_path)


def write_string_to_worksheet(worksheet, row, col, string):
    worksheet.write(row, col, string)
