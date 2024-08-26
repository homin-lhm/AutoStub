# AutoStub
http协议的自动化桩
## 桩的应用场景
比方说测试环境没法接入三方服务，如果想要保证服务的可测试性，开发有4种处理方案
① 写一个桩（假想的服务），一个空心服务，只能保证通信过程，固定返回200的处理结果
② 修改被测服务源码，屏蔽掉所有三方服务的交互代码
③ 写死三方服务的处理结果，不进行通信
④ 只提供线上环境来测试
## 这类型桩存在的痛点
① 三方服务异常的处理行为覆盖不到
② 定义的三方处理数据缺少真实性
③ 没法保障被测服务上线以后能和三方服务正常通信，还需要额外的线上调试成本
④ 开发不愿花更多的人力成本时间成本来保障可测试性
⑤ 线上测试的成本过高，或可能影响线上的真实数据
## 什么是自动化桩？
已知接口自动化框架的前提下，如果遇到了依赖服务异常的测试用例，没法落地成自动化脚本。
比方说：
背景-用户登录的场景，底层交互涉及到客户端、account用户服务、yzm验证码校验服务，account是我们的测试对象
用例名“请求登录接口，account处理超时” 操作步骤“step1-请求登录接口，step2-模拟account请求超时的情况，step3-校验登录接口的返回”期望值“返回状态码为500，返回体{"msg":"server error!"}”
自动化桩所提供的能力能将当前用例转换成自动化脚本！！
• 能够接受桩的消息进行校验，相当于验证被测服务请求三方服务协议的正确性！
• 测试用例能直接定义桩的结果返回！
自动化桩可以直接取代掉桩，开发没有额外的开发成本！！！
自动化桩还不需要开发进行部署，全程由测试操盘！！！！
## 实战演练
被测服务背景：多人文档编辑时，有一个痛点，B用户编辑的内容可能会覆盖A用户编辑的内容，所以提出编辑锁的方案，A用户进行文档A编辑后，不允许其他用户编辑同一个文档，B用户请求编辑接口会被拒绝。

展开服务端的测试工作，需要设计依赖服务异常的测试用例。
请求文档编辑接口，fileapp返回403的状态码  期望值：文档编辑接口返回 500状态码，返回体{XXXXXX}
请求文档编辑接口，fileapp返回超时  期望值：文档编辑接口返回 500状态码，返回体{XXXXXX}
请求文档编辑接口，fileapp异常下线  期望值：文档编辑接口返回 503状态码，返回体{XXXXXX}

![image](https://github.com/user-attachments/assets/fa317299-166a-460f-97bd-a950bf40f24a)

## 自动化桩实现的交互文档
![image](https://github.com/user-attachments/assets/ef20f522-6d14-4cb9-ab74-5458347f407c)
桩的交互流程：
step1：在python客户端实现socket服务端，提供通信方式
step2：在桩模块下，实现socket客户端，和python客户端的socket服务建立通信，明确channel并实例化。
step3：根据桩启动配置所描述的端口在桩模块基于flask框架启动http的桩，满足任意接口和任意请求方式。
step4：启动被测服务，满足依赖关系。
step5：测试用例开始执行，使用桩模块提供的异步http请求方法调用被测服务的接口。
step6：被测服务在入参协议校验完成后开始请求依赖服务获取业务的处理结果，被测服务调用依赖服务的接口（实际上就是请求桩）。
step7：桩服务会通过channel发送消息，将从被测服务接到的请求打包起来发送到python客户端的socket服务。
step8：python客户端会通过拉取消息的方式接收消息。
step9：python客户端需要定义桩的结果返回，定义完成通过socket提供的send进行消息的回调。
step10：桩接收到回调消息后包装成回调消息直接进行被测服务的消息回复。
step11：被测服务通过接口返回返回业务的处理结果。
step12：python客户端能正常完成用例的流转过程。
step13：python客户端执行完全量用例后下线桩服务。

## 自动化桩模块介绍
![image](https://github.com/user-attachments/assets/b3529335-13e8-42fe-add5-2b9099526569)
app -- 被测服务demo
business -- 接口自动化框架业务方法封装
common -- 接口自动化框架的通用方法封装
config -- 接口自动化框架的配置文件
httpStubFramework -- 自动化桩组件！！
  httpCommon -- 支持异步http请求和接受
  httpSeverStub -- 桩实例
  httpStubOperator -- 桩的操作方法
  serverStatusCheck -- 简易的服务状态检测方法
logs -- 接口自动化框架的日志存储
testCase -- 接口自动化框架的用例集
main -- 接口自动化框架的启动方法
report -- 接口自动化可视化报告
stub_instantiation -- 桩启动信息配置！！



## 自动化桩使用的协议：
### 桩的启动配置
配置文件类型：stub_instantiation.py
```python
from httpStubFramework.httpStubOperator import StubOperator  # 在该模块实现桩对象的实例化，需要导入模块下的类

### 每一个桩都需要先定义一套配置
stub_config = {
    'http_app_port': 8770,  # 定义了http桩实例的端口，ip默认本机
    'socket_client_port': 8771,  # 定义了桩通道通信过程socket的客户端端口
    'socket_server_port': 8772  # 定义了桩通道通信过程socket的服务端端口
}

# 如果要定义一个桩，可以根据桩的业务定义实例化的名称
fileAppStub = StubOperator(桩的配置信息)
```

### 桩启动方法（自动化框架执行入口main）
```python
from stub_instantiation import fileAppStub

fileAppStub.start_stub()
```

### 桩下线方法（自动化框架执行入口main）
```python
from stub_instantiation import fileAppStub

fileAppStub.shutdown_stub()
```
### 桩http异步方法应用（用例层在调用被测服务http接口时的接口调用方法）
```python
from httpCommon import HttpCommon

hc = HttpCommon()  # 使用前需要进行实例化
hc.http_requests()  # 发送http接口请求，实参传递满足requests.requests的形参

# 等http接口业务处理完成后
code = hc.status_code  # 获取接口返回的状态码
text = hc.res_text  # 获取接口返回的返回体文本
```


### 从桩接收消息（用例层）
```python
from stub_instantiation import fileAppStub

data = fileAppStub.receive()  # 接收桩受收到的请求协议消息接收消息模板：
{
    "body": dict(re_data),  # 收到的请求体
    "headers": dict(re_headers),  # 收到的请求头
    "cookies": dict(re_cookies),  # 收到的cookie
    "path": path,  # 收到的路由地址
    "method": re_method,  # 收到的请求方式
    "params": dict  # params参数，以字典形式返回
}
```

### 定义桩的结果返回（用例层）
```python
from stub_instantiation import fileAppStub

msg = {
    'body': {},  # 返回体在这一侧定义，目前只支持json返回体的返回
    'code': 200  # 定义了桩的返回状态码
}

fileAppStub.send(msg)  # 将定义好的返回体返回给桩
```
