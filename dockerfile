FROM python:2.7-slim

WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y gcc libmagic-dev libmagic1 git && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 暴露容器的8000端口到24150
EXPOSE 8000

# 容器运行时直接启动flask服务器
CMD ["python", "server.py"]