# 使用官方Python镜像作为基础
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 安装 Chrome 浏览器和依赖（简化版）
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    gnupg2 \
    unzip \
    fonts-wqy-zenhei \
    fonts-noto-cjk \
    libxss1 \
    libnss3 \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libatspi2.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libgtk-3-0 \
    libpango-1.0-0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    chromium \
    chromium-driver \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# 设置Chrome环境变量
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROME_DRIVER_PATH=/usr/bin/chromedriver

# 复制requirements.txt
COPY backend/requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目代码
COPY backend/ .

# 设置环境变量
ENV PYTHONPATH=/app
ENV DOCKER_ENV=true
ENV HEADLESS=true
ENV TEST_URL=http://localhost:8080
ENV TEST_USERNAME=13800138000
ENV TEST_PASSWORD=123456
ENV VERIFY_CODE=8888

# 运行时入口
ENTRYPOINT ["python", "main.py"]

# 默认命令（演示模式）
CMD ["--demo"]
