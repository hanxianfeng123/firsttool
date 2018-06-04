#!/usr/bin/env python
# coding:utf-8

__author__ = 'Richard.han'
__date__ = '2018-4-26'

import time
import datetime
import configparser
from configparser import MissingSectionHeaderError


def get_settings(filename):
    config = configparser.ConfigParser()
    try:
        config.read(filename, encoding='utf-8')
    except MissingSectionHeaderError:
        config.read(filename, encoding='utf-8-sig')
    return config


def get_thread_num_from_xml(jmx_file):
    import re
    pattern = r'.+name="ThreadGroup.num_threads">(.+)?<'
    with open(jmx_file, 'rb') as f:
        while True:
            line = f.readline().decode('utf-8')
            matched_object = re.search(pattern, line)
            if matched_object:
                return matched_object.group(1)


def TimeStampToTime(timestamp):
    timeStruct = time.localtime(timestamp)
    return time.strftime('%Y-%m-%d %H:%M:%S',timeStruct)

def get_FileModifyTime(filePath):
    import os
    time.ctime(os.stat(filePath).st_mtime)
    t = os.path.getmtime(filePath)
    return TimeStampToTime(t)

def save():
    # 存放日志
    import shutil
    import os
    import datetime

    config = get_settings("config.ini")
    folder_name = config['File']['APIName']

    log_path = config['File']['FilePath']
    log_name = config['File']['DownFile']
    jmx_name = config['File']['UpFile']
    jmx_file = os.path.join(log_path, jmx_name)
    thread_num = get_thread_num_from_xml(jmx_file)
    num = config['Load']['Num']
    thread_num = int(num)*int(thread_num)
    #parent_folder = r'D:\项目资料\三一上云\性能日志'
    dest_folder = os.path.join(log_path, folder_name, str(thread_num))
    print(dest_folder)
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    source_file = os.path.join(log_path, log_name)
    print(source_file)
    time_now = datetime.datetime.now()
    time_now = time_now.strftime('%Y-%m-%d %H-%M-%S-%f')[:-3]
    shutil.copy(source_file, dest_folder)
    print(os.path.join(dest_folder, log_name))
    print(os.path.join(dest_folder, time_now + ".jtl"))
    os.rename(os.path.join(dest_folder, log_name), os.path.join(dest_folder, time_now + ".jtl"))