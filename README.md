# T2-排行榜数据展示前后端

## 主要技术栈

前端 `React` + `Ant Design`

后端 `FastAPI` + `SQLAlchemy`

## 加密验证

前后端通信密码传输：`RSA`非对称加密算法，前端公钥，后端私钥

数据库存取密码：`AES`对称式加密算法

用户身份令牌(token)：`JWT` (因设计过期时间较为繁琐，这里先以永久token作demo展示)

## 如何运行

1. 来到"./here"文件夹

2. 在虚拟环境中运行指令

```sh
pip install -r reqirements.txt
uvicorn main:app --port 12345
```

3. 浏览器访问

<a href='http://localhost:12345/index.html'>http://localhost:12345/index.html</a>

## 操作相关

### 管理员

   账号 `123456`

   密码 `admin`

### 其他测试账号

密码统一为 `basketball`

账号为 `201800001111`, `201900002222`, `202000003333`, `202100004444`, `202200005555`

你也可以选择 **直接注册**

## 作者

钓乌龟的大攻稽 2023.10.27
