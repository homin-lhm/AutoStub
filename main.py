import unittest
import os
from BeautifulReport import BeautifulReport
from stub_instantiation import fileAppStub
import socket
from httpStubFramework.serverStatusCheck import status_check

DIR = os.path.dirname(os.path.abspath(__file__))
ENVIRON = 'Offline'  # 'Online' -> 线上环境， 'Offline' -> 测试环境

if __name__ == '__main__':
    # 启动桩
    fileAppStub.stub_start()
    # 启动被测服务 XXX，也可以手动启动

    status_check({'socket_channel', 'flask_app'})

    run_pattern = 'all'  # all 全量测试用例执行 /  smoking 冒烟测试执行  /  指定执行文件
    if run_pattern == 'all':
        pattern = 'test_*.py'
    elif run_pattern == 'smoking':
        pattern = 'test_major*.py'
    else:
        pattern = run_pattern + '.py'
    suite = unittest.TestLoader().discover('./testCase', pattern=pattern)

    result = BeautifulReport(suite)
    result.report(filename="report.html", description='测试报告', report_dir='./')

    # 桩下线
    fileAppStub.shutdown_stub()

