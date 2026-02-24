# 商城配置文件
# 支持 TPshop、ShopXO、LikeShop 等多种商城系统
# 根据实际部署的商城修改配置

import os

# ============================================================
# 商城类型配置
# 支持: tpshop, shopxo, likeshop, custom
# ============================================================
SHOP_TYPE = os.getenv("SHOP_TYPE", "tpshop")

# ============================================================
# TPshop 商城配置（默认）
# ============================================================
TPSHOP_CONFIG = {
    "name": "TPshop",
    "base_url": os.getenv("TEST_URL", "http://localhost:8080"),
    "login_path": "/index.php?m=user&a=login",
    "username": os.getenv("TEST_USERNAME", "13800138000"),
    "password": os.getenv("TEST_PASSWORD", "123456"),
    "verify_code": os.getenv("VERIFY_CODE", "8888"),
    "locators": {
        "login_link": "//a[contains(text(),'登录')]",
        "username_input": "username",  # name属性
        "password_input": "password",  # name属性
        "verify_code_input": "verify_code",  # name属性
        "login_button": "//a[@name='sbtbutton']",
        "error_message": "layui-layer-content",  # class属性
        "success_indicator": "//a[contains(text(),'退出')]",
    },
    "verify_code_enabled": True,
    "verify_code_type": "universal",  # universal=万能验证码, image=图片验证码
}

# ============================================================
# ShopXO 商城配置
# ============================================================
SHOPXO_CONFIG = {
    "name": "ShopXO",
    "base_url": os.getenv("TEST_URL", "http://localhost:8080"),
    "login_path": "/index.php?s=/index/user/logininfo.html",
    "username": os.getenv("TEST_USERNAME", "shopxo"),
    "password": os.getenv("TEST_PASSWORD", "shopxo"),
    "verify_code": os.getenv("VERIFY_CODE", ""),
    "locators": {
        "login_link": "//a[contains(@href,'logininfo')]",
        "username_input": "accounts",  # name属性
        "password_input": "pwd",  # name属性
        "verify_code_input": "verify",  # name属性
        "login_button": "//button[@type='submit']",
        "error_message": "am-alert",  # class属性
        "success_indicator": "//a[contains(text(),'退出')]",
    },
    "verify_code_enabled": False,
    "verify_code_type": "none",
}

# ============================================================
# LikeShop 商城配置
# ============================================================
LIKESHOP_CONFIG = {
    "name": "LikeShop",
    "base_url": os.getenv("TEST_URL", "http://localhost:8080"),
    "login_path": "/pc/login",
    "username": os.getenv("TEST_USERNAME", "13800138000"),
    "password": os.getenv("TEST_PASSWORD", "123456"),
    "verify_code": os.getenv("VERIFY_CODE", ""),
    "locators": {
        "login_link": "//a[contains(text(),'登录')]",
        "username_input": "account",  # name属性
        "password_input": "password",  # name属性
        "verify_code_input": "code",  # name属性
        "login_button": "//button[contains(text(),'登录')]",
        "error_message": "el-message__content",  # class属性
        "success_indicator": "//span[contains(text(),'退出')]",
    },
    "verify_code_enabled": False,
    "verify_code_type": "none",
}

# ============================================================
# 自定义商城配置（用户可自行修改）
# ============================================================
CUSTOM_CONFIG = {
    "name": "Custom",
    "base_url": os.getenv("TEST_URL", "http://localhost:8080"),
    "login_path": "/login",
    "username": os.getenv("TEST_USERNAME", "admin"),
    "password": os.getenv("TEST_PASSWORD", "admin123"),
    "verify_code": os.getenv("VERIFY_CODE", ""),
    "locators": {
        "login_link": "//a[contains(text(),'登录')]",
        "username_input": "username",
        "password_input": "password",
        "verify_code_input": "captcha",
        "login_button": "//button[@type='submit']",
        "error_message": "error",
        "success_indicator": "//a[contains(text(),'退出')]",
    },
    "verify_code_enabled": False,
    "verify_code_type": "none",
}

# ============================================================
# 获取当前商城配置
# ============================================================
def get_shop_config():
    """根据 SHOP_TYPE 返回对应的商城配置"""
    configs = {
        "tpshop": TPSHOP_CONFIG,
        "shopxo": SHOPXO_CONFIG,
        "likeshop": LIKESHOP_CONFIG,
        "custom": CUSTOM_CONFIG,
    }
    return configs.get(SHOP_TYPE.lower(), TPSHOP_CONFIG)

# 当前使用的配置
SHOP_CONFIG = get_shop_config()

# ============================================================
# 通用配置
# ============================================================
# 浏览器配置
HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
BROWSER_TYPE = os.getenv("BROWSER_TYPE", "chrome")  # chrome, firefox, edge
IMPLICIT_WAIT = int(os.getenv("IMPLICIT_WAIT", "10"))
EXPLICIT_WAIT = int(os.getenv("EXPLICIT_WAIT", "10"))
PAGE_LOAD_TIMEOUT = int(os.getenv("PAGE_LOAD_TIMEOUT", "30"))

# 截图配置
SCREENSHOT_ON_FAILURE = True
SCREENSHOT_ON_SUCCESS = True
SCREENSHOT_DIR = os.path.join(os.path.dirname(__file__), "reports", "screenshots")

# 日志配置
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.path.join(os.path.dirname(__file__), "reports", "test.log")

# ============================================================
# 快捷访问（兼容旧代码）
# ============================================================
TEST_URL = SHOP_CONFIG["base_url"]
TEST_USERNAME = SHOP_CONFIG["username"]
TEST_PASSWORD = SHOP_CONFIG["password"]
UNIVERSAL_VERIFY_CODE = SHOP_CONFIG["verify_code"]
