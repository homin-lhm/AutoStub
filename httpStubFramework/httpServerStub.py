from flask import Flask, request, jsonify
import socket
from httpStubFramework.serverStatusCheck import check_server
import os
import signal
import json
from werkzeug.serving import make_server


clientSocket = None


class HttpStub:
    app = Flask(__name__)

    def __init__(self, http_port, socket_client_port, socket_server_port):
        self.client_socket = None
        self.http_port = http_port
        self.socket_client_port = socket_client_port
        self.socket_server_port = socket_server_port
        pass

    def socket_client_start(self):
        """桩服务实例化socket客户端"""
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        client_address = ('localhost', self.socket_client_port)
        self.client_socket.bind(client_address)
        server_address = ("localhost", self.socket_server_port)
        self.client_socket.connect(server_address)
        return self.client_socket

    @staticmethod
    @app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
    def msg_collect(path):
        """http桩，兼容所有路由和请求方式"""
        try:
            re_method = request.method
            # 实现桩下线的方法，提供下线的接口shutdown
            if path == 'shutdown' and re_method == 'POST':
                os.kill(os.getpid(), signal.SIGINT)
                return 'Server shutting down...', 200

            # 实现http接口请求获取请求数据的通用方法
            re_headers = request.headers
            re_cookies = request.cookies
            params = dict(request.args)
            # re_data = request.data
        except Exception as e:
            print(e)
            return {}, 888

        # 打包桩接收到的请求数据
        receive_msg = {
            # "body": json.loads(re_data),
            "headers": dict(re_headers),
            "cookies": dict(re_cookies),
            "path": path,
            "method": re_method,
            'params': params
        }
        message = json.dumps(receive_msg)
        # 将桩收到的请求打包发送到socket通道，测试用例可以从channel recv下来
        clientSocket.sendall(message.encode("utf-8"))

        # 测试用例定义了桩的结果返回，结果返回需要通过channel传输到桩实例，桩实例用socket client 来recv
        data = clientSocket.recv(1024).decode("utf-8")
        send_data = json.loads(data)
        send_response = send_data["body"]
        send_status_code = send_data["code"]
        return send_response, send_status_code

    def server_run(self):
        """http桩启动"""
        global clientSocket
        clientSocket = self.socket_client_start()
        server = make_server('0.0.0.0', self.http_port, self.app)
        check_server.add('flask_app')
        server.serve_forever()
