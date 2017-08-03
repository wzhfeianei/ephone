"""
Author:weizhanfei
Created:2017/7/22
Purpose:
"""
import os.path as p
import os


def create_dir(path):
    if not p.exists(path):
        os.makedirs(path)


def get_all_file(path, filter_file=""):
    file_list = []
    for root, dirs, files in os.walk(path):
        for f in files:
            if filter_file == "":
                file_list.append(p.join(root, f))
            else:
                if filter_file in f:
                    file_list.append(p.join(root, f))
    return file_list


if __name__ == '__main__':
    get_all_file("d:\\")
