import time
import datetime
import os
from colorama import Fore, init
import inspect
import functools

now_dir = os.path.dirname(__file__)  # 获取主目录路径
now_time = datetime.datetime.now()
str_time = now_time.strftime("%Y-%m-%d")


def info_log(text):
    log_dir = now_dir + '/logs/'
    date = time.strftime('%H:%M:%S', time.localtime(time.time()))
    microsecond = datetime.datetime.now().strftime('%f')[:3]
    stack = inspect.stack()  # 获取方法执行的代码路径
    code_path = f"{os.path.basename(stack[1].filename)}:{stack[1].lineno}"
    log_text = "[INFO]{}-{}-{}\n".format(code_path, (date + '.' + microsecond), text)
    # print(Fore.GREEN + log_text.strip())
    log_name = "{}_info.log".format(str_time)
    with open(log_dir + log_name, mode="a", encoding="utf-8") as f:
        f.write(log_text)


def error_log(text):
    log_dir = now_dir + '/logs/'
    date = time.strftime('%H:%M:%S', time.localtime(time.time()))
    microsecond = datetime.datetime.now().strftime('%f')[:3]
    stack = inspect.stack()  # 获取方法执行的代码路径
    code_path = f"{os.path.basename(stack[1].filename)}:{stack[1].lineno}"
    log_text = "[ERROR]{}-{}-{}\n".format(code_path, (date + '.' + microsecond), text)
    # print(Fore.RED + str(log_text).strip())
    log_name = "{}_error.log".format(str_time)
    with open(log_dir + log_name, "a", encoding="utf-8") as f:
        f.write(log_text)


def warning_log(text):
    log_dir = now_dir + '/logs/'
    date = time.strftime('%H:%M:%S', time.localtime(time.time()))
    microsecond = datetime.datetime.now().strftime('%f')[:3]
    stack = inspect.stack()  # 获取方法执行的代码路径
    code_path = f"{os.path.basename(stack[1].filename)}:{stack[1].lineno}"
    log_text = "[WARN]{}-{}-{}\n".format(code_path, (date + '.' + microsecond), text)
    # print(Fore.BLUE + str(log_text).strip())
    log_name = "{}_warn.log".format(str_time)
    with open(log_dir + log_name, "a", encoding="utf-8") as f:
        f.write(log_text)
