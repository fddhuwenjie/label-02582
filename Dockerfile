# Dockerfile for TPshop Automation Test Framework
# 使用Ubuntu 22.04基础镜像（稳定且Chrome支持良好）
FROM ubuntu:22.04

# 设置工作目录
WORKDIR /app

# 设置环境变量 - 禁用Python字节码缓存、启用无缓冲输出
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    TZ=Asia/Shanghai

# 安装系统依赖和Chromium浏览器（支持多架构）
RUN apt-get update && apt-get install -y --no-install-recommends \
    tzdata \
    python3 \
    python3-pip \
    python3-venv \
    wget \
    curl \
    gnupg \
    unzip \
    chromium-browser \
    chromium-chromedriver \
    --fix-missing \
    && rm -rf /var/lib/apt/lists/*

# 创建Python软链接
RUN ln -sf /usr/bin/python3 /usr/bin/python && \
    ln -sf /usr/bin/pip3 /usr/bin/pip

# 升级pip
RUN pip install --no-cache-dir --upgrade pip

# 复制 requirements.txt 并安装Python依赖
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目代码
COPY backend/ .

# 设置默认环境变量（可在运行时覆盖）
ENV TEST_URL="http://localhost:8080" \
    BROWSER="chromium" \
    HEADLESS="true" \
    TEST_USERNAME="13800138000" \
    TEST_PASSWORD="123456" \
    VERIFY_CODE="8888" \
    LOG_LEVEL="INFO" \
    CHROME_BIN="/usr/bin/chromium-browser" \
    CHROMEDRIVER_PATH="/usr/bin/chromedriver"

# 运行测试（默认命令）
CMD ["python", "main.py"]
