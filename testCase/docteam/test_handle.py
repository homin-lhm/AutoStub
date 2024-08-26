import unittest
import requests
import time
import json
# from businessCommon.data_clear import clear_groups
from common.checkOutput import CheckPro
from common.caseLogs import info, error, step, class_case_log
from businessCommon.dataClear import file_user_clear
from common.yamlRead import YamlRead
from httpStubFramework.httpCommon import HttpCommon
from stub_instantiation import fileAppStub


class DocTeamHandle(unittest.TestCase):
    file_id = '188'

    def setUp(self) -> None:
        file_user_clear(self.file_id)

    def testCase01(self):
        """fileApp返回超时"""
        step('A用户请求编辑锁协作接口')
        headers = {'Content-Type': 'application/json', 'Cookie': 'user_id=A'}
        body = {
            "file_id": self.file_id,
            "status": "edit"
        }
        hc = HttpCommon()
        hc.http_requests(method='post', url='http://192.168.1.14:8530/edit', headers=headers, json=body)

        stub_recv_data = fileAppStub.receive()
        self.assertEqual('file', stub_recv_data['path'])
        self.assertEqual({'file_id': self.file_id}, stub_recv_data['params'])

        msg = {
            'body': {"msg": "success"},  # 返回体在这一侧定义，目前只支持json返回体的返回
            'code': 200  # 定义了桩的返回状态码
        }
        time.sleep(4)
        fileAppStub.send(msg)
        info(hc.status_code)
        info(hc.res_text)
        self.assertEqual(504, hc.status_code)
        expected = {
            'msg': "SERVER TIMEOUT"
        }
        CheckPro().check_output(expected=expected, actual=json.loads(hc.res_text))

    def testCase02(self):
        """fileApp返回错误状态码"""
        step('A用户请求编辑锁协作接口')
        headers = {'Content-Type': 'application/json', 'Cookie': 'user_id=A'}
        body = {
            "file_id": self.file_id,
            "status": "edit"
        }
        hc = HttpCommon()
        hc.http_requests(method='post', url='http://192.168.1.14:8530/edit', headers=headers, json=body)

        stub_recv_data = fileAppStub.receive()
        self.assertEqual('file', stub_recv_data['path'])
        self.assertEqual({'file_id': self.file_id}, stub_recv_data['params'])

        msg = {
            'body': {"msg": "success"},  # 返回体在这一侧定义，目前只支持json返回体的返回
            'code': 403  # 定义了桩的返回状态码
        }
        fileAppStub.send(msg)
        info(hc.status_code)
        info(hc.res_text)
        self.assertEqual(500, hc.status_code)
        expected = {
            'msg': "SERVER ERROR"
        }
        CheckPro().check_output(expected=expected, actual=json.loads(hc.res_text))
