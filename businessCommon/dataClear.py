import requests


def file_user_clear(file_id):
    """清空文件的协作用户"""
    headers = {'Content-Type': 'application/json'}
    body = {
        "file_id": file_id
    }
    requests.delete(url='http://192.168.1.14:8530/clear', headers=headers, json=body)
