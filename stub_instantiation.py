from httpStubFramework.httpStubOperator import StubOperator  # 在该模块实现桩对象的实例化，需要导入模块下的类

# 每一个桩都需要先定义一套配置
stub_config = {
    'http_app_port': 8770,  # 定义了http桩实例的端口，ip默认本机
    'socket_client_port': 8771,  # 定义了桩通道通信过程socket的客户端端口
    'socket_server_port': 8772  # 定义了桩通道通信过程socket的服务端端口
}

# 如果要定义一个桩，可以根据桩的业务定义实例化的名称
fileAppStub = StubOperator(http_port=stub_config['http_app_port'], socket_client_port=stub_config['socket_client_port'],
                           socket_server_port=stub_config['socket_server_port'])
