# AWVS MCP

基于python实现的Acunetix Web Vulnerability Scanner (AWVS)扫描器MCP。

## 功能特点

- 支持Stdio和SSE两种模式
- 批量添加URL到AWVS扫描器并进行扫描
- 支持多种扫描类型：完全扫描、高风险漏洞扫描、XSS漏洞扫描、SQL注入漏洞扫描等
- 支持清空扫描任务和目标
- 自定义扫描参数

## 安装

```bash
git clone https://github.com/JishiTeam/python_awvs_server
```

## 环境依赖

```markdown
Python 3.12
```

## 使用方法

### 配置

使用前需要在main.py中配置AWVS API的地址和API密钥：

```json
ACUNETIX_API_URL = "https://localhost:3443/api/v1"
ACUNETIX_API_KEY = "your_api_key_here"
```

### 本地启动服务

```bash
pip install -r requirements.txt
python main.py
```

服务将启动并监听8000端口。

## 容器启动

```
docker-compose up -d
```



## API工具

本MCP实现提供以下功能：

- 添加URL并开始扫描
- 列出所有扫描目标
- 列出所有扫描任务
- 删除所有目标和扫描任务
- 仅删除扫描任务
- 对已有目标开始新的扫描
- 获取扫描结果（包括漏洞信息、技术信息、爬取数据、统计信息）

