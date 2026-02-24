"""
配置文件
"""
import os

# 测试网站地址
BASE_URL = os.getenv("TEST_URL", "http://localhost:8080")

# 浏览器配置
BROWSER = os.getenv("BROWSER", "chrome")
HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"

# 超时配置
IMPLICIT_WAIT = 10
EXPLICIT_WAIT = 10
PAGE_LOAD_TIMEOUT = 30

# 测试账号
TEST_USER = {
    "username": "13800138000",
    "password": "123456",
    "verify_code": "8888"
}

# 报告配置
REPORT_DIR = os.path.join(os.path.dirname(__file__), "reports")
