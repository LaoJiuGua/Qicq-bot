# Qicq-Bot

## 简介

一个基于[Fastapi](https://fastapi.tiangolo.com/)插件化的Python版本QQ机器人封装.

交流群：[Qicq-bot交流群](https://jq.qq.com/?_wv=1027&k=QR1bHfUs)

* 目标：
  * 热插拔
  * 热加载
  * QQ群组管理功能
  * QQ管理功能
  * 多QQ管理功能
  * ....暂时就想了这么多(后期在补)....
* 现状：
  * 冷插拔
  * 冷加载


### 生命周期
`触发对话`--->`消息接收`---->`消息分级`---->`执行插件`---->`返回消息`

> 因为聊天的每次对话都在在同一个接口进行，所以在`消息接受`和`消息分级`的时候都是在寻找需要执行得`插件`，在发送人和机器人的每一回合对话我都当作一个`指令`或者一段`程序`得`生命周期`.

---

## 依赖
[![go-cqhttp](https://camo.githubusercontent.com/c357af8fb57e5ee23e9895009f31f2af6d8fcefe9b01b909357226584ce54818/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f762f72656c656173652f4d727334732f676f2d6371687474703f636f6c6f723d626c756576696f6c657426696e636c7564655f70726572656c6561736573)](https://docs.go-cqhttp.org/)
[![OneBot](https://camo.githubusercontent.com/2404dd66111fb673238599b68eda517eb6df44da2329f20522c1d9570f3a5671/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f4f6e65426f742d7631312d626c75653f7374796c653d666c6174266c6f676f3d646174613a696d6167652f706e673b6261736536342c6956424f5277304b47676f414141414e5355684555674141414541414141424142414d414141425952327a74414141414956424d56455541414141414141414441774d4842776365486834554642514e4451305a47526b6f4b4367764c79386949694c57536457594141414141585253546c4d41514f62595a6741414151564a52454655534d66746c4d3052676a415168562b304154594b36693158622b694d643071674245716742457577424f78553251444b736a766f6a5150766b4a2f5a4c3573586b6757724669724b344d696259556445334f52326e4570754b7a312f713843644e784e516774685a435859564c6a796f44516674614b756e69484857526e506832474355657452322f3948734d4158795554342f33554877745154324167675343474b65534173466e7842494f75416767646833414b544c3770447543794142634d623061515037614d34416e4162632f7748774135443277444854546535366749494f55412f3459595632653173673731335058645a4a41756e63645a4d41476b41756b55394f416e34304f3834392b306f726e50775439337270685746306d67416261755572454f74686c58385a7537503541366b5a794b434a793735686877314d6772395241557658374133637347715a656745646e69437833306333616741414141424a52553545726b4a6767673d3d)](https://github.com/botuniverse/onebot/blob/main/README.md)

[![Fastapi](https://camo.githubusercontent.com/86d9ca3437f5034da052cf0fd398299292aab0e4479b58c20f2fc37dd8ccbe05/68747470733a2f2f666173746170692e7469616e676f6c6f2e636f6d2f696d672f6c6f676f2d6d617267696e2f6c6f676f2d7465616c2e706e67)](https://github.com/tiangolo/fastapi)

---

## 灵感来源
- ![ChatGPT Mirai QQ Bot](https://camo.githubusercontent.com/345a7bfe8d089531f2dc52c5e0326f7e4c097da58db2ceb976e078be35c0e50d/68747470733a2f2f62616467656e2e6e65742f6769746875622f73746172732f6c73733233332f636861746770742d6d697261692d71712d626f743f69636f6e3d676974687562266c6162656c3d7374617273) [ChatGPT Mirai QQ Bot](https://github.com/LaoJiuGua/chatgpt-mirai-qq-bot)
  - **消息转图片**基于此项目之上进行修改
---

## 目录

```
Qicq-bot
 ├── api
 │   └── v1
 ├── cqhttp
 │   ├── api.py
 │   ├── request_model.py
 │   └── resp_model.py
 ├── message
 ├── PluginFrame
 │   ├── PluginManager
 │   ├── Plugins
 │   └── plugins_conf.py
 ├── sk
 ├── static
 ├── utils
 │   ├── simple_to_img.py  
 │   └── text_to_img.py
 ├── globe.py
 ├── config.py
 ├── config.yaml
 └── main.py
 
 # api： fastapi的接口封装
 # cqhttp： cqhttp相关封装
     # api.py：cqhttp请求API常量封装
     # request_model.py： cqhttp请求API的参数封装
     # cq_code.py： cq_code消息封装(发送qq消息时使用)
     # resp_model.py： cqhttp请求API的返回体封装
 # PluginFrame： 插件相关目录
     # PluginManager：插件管理封装目录
     # Plugins：插件代码存放目录（PluginManager会自动扫描插件）
     # plugins_conf：插件配置文件(封装支持正则指令匹配，装饰器为插件赋予指令)
     # main.py： 暂时没用
 # sk：websocket操作封装目录
 # static：静态文件目录
 # utils：工具目录
     # simple_to_img.py：简单的文字转图片
     # text_to_img.py：文字转图片
 # globe.py：公共常量/变量定义文件--如：socket链接对象
 # config.yaml：项目配置文件
  # config.py：项目配置文件读取封装
 # main.py：项目启动文件
 
 还差一个关键性项目配置文件（后期在补上）
```

---

## 使用`Qicq-bot`

- 第一步：安装Python >= 3.10
- 第二步：安装go-cqhttp并选择反向链接
  - 修改生成config文件的帐号相关
  - 修改生成config文件的服务器相关{`ws-reverse.universal`修改成(`ws://host:port/ws`)}
- 第三步：pip install -r requirements.txt
- 第四步：python main.py

---

声明：本人由于工作时间不定，实际独自开发时间少，功能不全情况下请谅解，后期会慢慢补.
最近一段时间会尽量将基础功能完善