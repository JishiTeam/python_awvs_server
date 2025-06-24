# 使用官方 Python 3.12 镜像作为基础镜像
FROM python:3.12-slim

# 设置工作目录
WORKDIR /app

# 将当前目录下的所有文件复制到工作目录
COPY . /app

# 安装依赖（如果有requirements.txt文件）
RUN pip install --no-cache-dir -r requirements.txt

# 暴露容器的8000端口
EXPOSE 8000

# 启动应用
CMD ["python", "main.py"]