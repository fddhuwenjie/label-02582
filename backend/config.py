"""
配置文件 - TPshop商城自动化测试配置
"""
import os

# ==================== 测试环境配置 ====================
# TPshop商城部署地址
# 本地部署: http://localhost:8080
# Docker部署: http://tpshop:80
# 远程服务器: http://your-server-ip:port
BASE_URL = os.getenv("TEST_URL", "http://localhost:8080")

# ==================== 浏览器配置 ====================
BROWSER = os.getenv("BROWSER", "chrome")
HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"

# ==================== 超时配置 ====================
IMPLICIT_WAIT = 10
EXPLICIT_WAIT = 10
PAGE_LOAD_TIMEOUT = 30

# ==================== 测试账号配置 ====================
TEST_USER = {
    "username": os.getenv("TEST_USERNAME", "13800138000"),
    "password": os.getenv("TEST_PASSWORD", "123456"),
    "verify_code": os.getenv("TEST_VERIFY_CODE", "8888")  # TPshop万能验证码
}

# ==================== 验证码配置 ====================
# TPshop商城在测试环境下可配置万能验证码
# 生产环境需要对接验证码识别服务或禁用验证码
UNIVERSAL_VERIFY_CODE = os.getenv("VERIFY_CODE", "8888")
# 是否跳过验证码验证（需要TPshop后台配置支持）
SKIP_VERIFY_CODE = os.getenv("SKIP_VERIFY_CODE", "false").lower() == "true"

# ==================== 报告配置 ====================
REPORT_DIR = os.path.join(os.path.dirname(__file__), "reports")
SCREENSHOT_DIR = os.path.join(REPORT_DIR, "screenshots")

# 确保目录存在
os.makedirs(REPORT_DIR, exist_ok=True)
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

# ==================== 日志配置 ====================
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
