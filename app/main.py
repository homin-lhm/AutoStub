import coverage
import time
import threading
import os


cov = coverage.coverage()  # 实例化
cov.start()  # 开始统计


def app_run():
    from docteamApp import app
    app.run(port=8666, debug=True, use_reloader=False)


# 结束统计
def for_arg():
    while True:
        s = input("退出输入Q + Enter：")
        if s.lower() == "q":
            cov.stop()

            # 结果保存
            cov.save()

            # 命令行模式展示结果
            cov.report()

            # 生成HTML覆盖率报告
            cov.html_report(directory='result_html')
            print("zzz")
            os.kill(os.getpid(), 2)


t1 = threading.Thread(target=app_run)
t3 = threading.Thread(target=for_arg)

t1.start()
t3.start()

