import requests
from flask import Flask, request
from dbutils.pooled_db import PooledDB
import pymysql
import os
import signal
import yaml
import time
import multiprocessing
from customs_logs import info_log, error_log, warning_log
import redis
from aes_han import AesHandles

with open(file='./config.yml', mode="r", encoding="utf-8") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

app = Flask(__name__)

# key = "hominhominhominQ"
# iv = "uiuiuiuiabababab"
# aseHandle = AesHandles(key, iv)

# redis_conn = redis.Redis(
#     host="10.0.12.10",
#     port=6379,
#     db=1,
#     password="3558hominT."
# )
# 定义数据库连接池
pool = PooledDB(
    creator=pymysql,
    maxconnections=config["MaxConnections"],  # 连接池中最大连接数
    mincached=10,  # 初始化时连接池中的连接数
    maxcached=100,  # 连接池中最多保留的连接数
    blocking=False,  # 当连接池中没有可用连接时是否阻塞等待 True 就会等待
    maxusage=None,  # 一个连接最多被使用的次数，None 表示无限制
    autocommit=True,  # 都会自动提交事务
    setsession=[],  # 在连接中执行的 sql 命令
    maxshared=1,
    ping=0,  # ping 数据库服务器的时间间隔，0 表示不 ping
    host=config["MYSQL_HOST"],
    port=config["MYSQL_PORT"],
    user=config["MYSQL_USER"],
    password=config["MYSQL_PASSWORD"],
    database=config["MYSQL_DB"],
    charset=config["MYSQL_CHARSET"]
)


def data_check(actual_body):
    expected_body = {
        "file_id": {"type": str, "option": False, "length": 10},
        "status": {"type": str, "option": False, "length": 10}
    }
    for k, v in expected_body.items():
        if v["option"] is False:
            if k not in actual_body.keys():
                return False
        else:
            if k not in actual_body.keys():
                continue
        if type(actual_body[k]) != v["type"]:
            return False
        if type(actual_body[k]) == str:
            if len(actual_body[k]) > v["length"]:
                return False
        elif type(actual_body[k]) == int:
            if actual_body[k] > v["length"]:
                return False

    return True


def get_data_check(actual_body):
    expected_body = {
        "file_id": {"type": str, "option": False, "length": 50}
    }
    for k, v in expected_body.items():
        if v["option"] is False:
            if k not in actual_body.keys():
                return False
        else:
            if k not in actual_body.keys():
                continue
        if type(actual_body[k]) != v["type"]:
            return False
        if type(actual_body[k]) == str:
            if len(actual_body[k]) > v["length"]:
                return False
        elif type(actual_body[k]) == int:
            if actual_body[k] > v["length"]:
                return False

    return True

#
# # 限流装饰器 限流对象是单一客户端的请求数
# def rate_limiter(max_requests, time_period):
#     def decorator(func):
#         def wrapper(*args, **kwargs):
#             client_ip = request.remote_addr
#             key = f'rate_limit:{client_ip}'
#             current = int(redis_conn.get(key) or 0)
#
#             if current >= max_requests:
#                 response = {
#                     'error': 'Too many requests. Please try again later.'
#                 }
#                 response.status_code = 429
#                 return response
#
#             redis_conn.set(key, current + 1, ex=time_period, nx=True)
#             redis_conn.incr(key, 1)
#             return func(*args, **kwargs)
#
#         return wrapper
#
#     return decorator


@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_password = request.form.get('password')
    if shutdown_password == config['SHUTDOWN_PASSWORD']:
        info_log('Shutting down the server...')
        os.kill(os.getpid(), signal.SIGINT)
        return 'Server shutting down...', 200
    else:
        warning_log('Incorrect shutdown password')
        return 'Incorrect password', 403


@app.route("/clear", methods=['DELETE'])
def clear():
    data = request.json
    file_id = data['file_id']
    conn = pool.connection()
    cursor = conn.cursor()
    try:
        delete_sql = f"DELETE FROM doct WHERE file_id = {file_id}"
        cursor.execute(delete_sql)
        conn.commit()
    except Exception as error:
        print(f"Error: {error}")
        return {"msg": f"delete error"}, 403
    finally:
        cursor.close()
        conn.close()
    return {"msg": f"delete success"}, 200


# @rate_limiter(max_requests=10, time_period=60)
@app.route("/edit", methods=["POST"])
def edit():
    data = request.json
    cookie = request.cookies

    re_id = str(int(time.time() * 1000)) + '_id'
    info_log(f"user ip:{request.remote_addr}, re_id:{re_id}")
    # 入参校验
    try:
        info_log(f"re_id: {re_id}, log: {data}")
        info_log(f"re_id: {re_id}, log: {cookie}")
        check_res = data_check(data)
        if check_res is False:
            raise ValueError("check error")
        file_id = data["file_id"]
        status = data["status"]
        user_id = cookie["user_id"]
    except Exception as e:
        error_log(f"re_id: {re_id}, error: {e}")
        return {"msg": f"data error, msg: {e}"}, 400

    # 校验文件是否存在
    info_log(f"re_id: {re_id}, log: {'check file'}")

    try:

        print(f"{config['FILE_APP_HOST']}/file?file_id={file_id}")
        res = requests.get(url=f"{config['FILE_APP_HOST']}/file?file_id={file_id}", timeout=3)

        print(res.status_code)
        if res.status_code == 200:
            pass
        elif res.status_code == 403:
            error_log(f"re_id: {re_id}, error: file server response code - {res.status_code}, response body - {res.text}")
            return {"msg": f"SERVER ERROR"}, 500
    except requests.exceptions.ReadTimeout:
        return {"msg": f"SERVER TIMEOUT"}, 504
    # 数据处理
    info_log(f"re_id: {re_id}, log: {'sql handles'}")
    conn = pool.connection()
    cursor = conn.cursor()
    if status == "edit":
        sql = "SELECT * FROM doct WHERE file_id = %s and status = %s"
        val = (file_id, status)
        cursor.execute(sql, val)
        res = cursor.fetchone()
        info_log(f"re_id: {re_id}, log: {'sql res-'} {res}")
        if res is None:
            sql = "INSERT INTO doct (file_id, user_id, status) VALUES (%s, %s, %s)"
            val = (file_id, user_id, status)
            cursor.execute(sql, val)
            conn.commit()
            cursor.close()
            conn.close()
            return {"msg": "edit success"}, 200

        else:
            edit_user_id = res[1]
            cursor.close()
            conn.close()
            return {"msg": f"edit fail, {edit_user_id} edit ing"}, 403
    else:
        sql = "SELECT * FROM doct WHERE file_id = %s and status = %s and user_id = %s"
        val = (file_id, status, user_id)
        cursor.execute(sql, val)
        res = cursor.fetchone()
        info_log(f"re_id: {re_id}, log: {'sql res-'} {res}")
        if res is None:
            sql = "INSERT INTO doct (file_id, user_id, status) VALUES (%s, %s, %s)"
            val = (file_id, user_id, status)
            cursor.execute(sql, val)
            conn.commit()
            cursor.close()
            conn.close()
            return {"msg": f"operation success"}, 200
        else:
            return {"msg": f"operation fail, you exits use the file"}, 403


@app.route("/query", methods=["GET"])
def query():
    data = request.args
    cookie = request.cookies
    print(data)
    print(cookie)
    re_id = str(int(time.time() * 1000)) + '_id'
    info_log(f"user ip:{request.remote_addr}, re_id:{re_id}")
    # 入参校验
    try:
        info_log(f"re_id: {re_id}, log: {data}")
        info_log(f"re_id: {re_id}, log: {cookie}")
        check_res = get_data_check(data)
        if check_res is False:
            raise ValueError("check error")
        file_id = data["file_id"]

        # file_id = aseHandle.decrypt(file_id)
    except Exception as e:
        error_log(f"re_id: {re_id}, error: {e}")
        return {"msg": f"data error, msg: {e}"}, 400

    # 数据处理
    info_log(f"re_id: {re_id}, log: {'sql handles'}")
    conn = pool.connection()
    cursor = conn.cursor()

    print(file_id)
    sql = "SELECT * FROM doct WHERE file_id = %s"
    val = (file_id,)
    cursor.execute(sql, val)
    res = cursor.fetchall()
    print(res)
    data_res = []
    for i in res:
        one_data = {
            "file_id": i[0],
            "user_id": i[1],
            "status": i[2]
        }
        data_res.append(one_data)
    response_body = {
        "msg": "success",
        "data": data_res
    }
    cursor.close()
    conn.close()
    return response_body, 200


# def run_server():
#     app.run(port=config["SERVER_PORT"], debug=True, use_reloader=False)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=config["SERVER_PORT"], debug=True)
