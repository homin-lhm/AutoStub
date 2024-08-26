import socket
from threading import Thread
from httpStubFramework.httpServerStub import HttpStub
import requests
import time
import json
from httpStubFramework.serverStatusCheck import check_server


class StubOperator:
    def __init__(self, http_port, socket_client_port, socket_server_port):
        self.socket_server_port = socket_server_port
        self.socket_client_port = socket_client_port
        self.http_port = http_port
        self.server_socket = None
        self.client_socket = None

    def server_socket_start(self):
        """桩socket客户端的启动"""
        self.client_socket, client_address = self.server_socket.accept()
        check_server.add('socket_channel')

    def stub_start(self):
        """http桩初始化"""
        # 建立socket服务端
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_address = ('localhost', self.socket_server_port)
        self.server_socket.bind(server_address)
        self.server_socket.listen(1)

        # 桩应用的实例化
        http_stub = HttpStub(self.http_port, self.socket_client_port, self.socket_server_port)
        # 桩实例启动socket的客户端和app的启动
        stub_app_t = Thread(target=http_stub.server_run)
        stub_app_t.start()

        # 建立socket通道
        channel_t = Thread(target=self.server_socket_start)
        channel_t.start()

    def shutdown_stub(self):
        """http桩下线"""
        requests.post(url=f"http://127.0.0.1:{self.http_port}/shutdown", timeout=3)
        self.client_socket.close()
        self.server_socket.close()

    def receive(self):
        """http桩mock消息接收"""
        data = self.client_socket.recv(1024).decode("utf-8")
        return json.loads(data)

    def send(self, data):
        """http桩mock消息发送"""
        data = json.dumps(data)
        self.client_socket.sendall(data.encode("utf-8"))
        time.sleep(2)
