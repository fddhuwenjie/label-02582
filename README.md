# 商城登录功能自动化测试

基于 PO（Page Object）设计模式 + DDT 数据驱动的自动化测试框架，支持多种商城系统的登录功能测试。

## ⚠️ 重要说明

本项目是一个**通用的商城登录自动化测试框架**，支持以下商城系统：

| 商城系统 | 配置名称 | 说明 |
|----------|----------|------|
| TPshop | `tpshop` | 默认配置，需要自行部署 |
| ShopXO | `shopxo` | 开源商城，需要自行部署 |
| LikeShop | `likeshop` | 开源商城，需要自行部署 |
| 自定义 | `custom` | 可配置任意商城 |

**注意**：由于公开演示站点不稳定或不可用，本项目需要用户自行部署商城环境进行测试。

## 🔧 快速配置

### 方式一：环境变量配置

```bash
# 选择商城类型
export SHOP_TYPE="tpshop"  # tpshop, shopxo, likeshop, custom

# 配置商城地址和账号
export TEST_URL="http://your-shop-url.com"
export TEST_USERNAME="13800138000"
export TEST_PASSWORD="123456"
export VERIFY_CODE="8888"  # TPshop万能验证码

# 运行测试
cd backend
python -m pytest tests/test_login.py -v
```

### 方式二：修改配置文件

编辑 `backend/shop_config.py`，修改对应商城的配置：

```python
TPSHOP_CONFIG = {
    "base_url": "http://your-tpshop-url.com",
    "username": "your_username",
    "password": "your_password",
    "verify_code": "8888",
    # ...
}
```

## 📦 支持的商城配置

### TPshop 配置（默认）

```bash
export SHOP_TYPE="tpshop"
export TEST_URL="http://localhost:8080"
export TEST_USERNAME="13800138000"
export TEST_PASSWORD="123456"
export VERIFY_CODE="8888"
```

**TPshop 部署参考**：详见 `docs/TPSHOP_DEPLOY.md`

### ShopXO 配置

```bash
export SHOP_TYPE="shopxo"
export TEST_URL="http://localhost:8080"
export TEST_USERNAME="shopxo"
export TEST_PASSWORD="shopxo"
```

### 自定义商城配置

编辑 `shop_config.py` 中的 `CUSTOM_CONFIG`，配置你的商城元素定位器。

## 🚀 运行测试

### 1. 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

### 2. 配置商城环境

确保你有一个可访问的商城环境，并配置好环境变量或修改配置文件。

### 3. 运行测试

```bash
# 演示模式（无需商城环境）
python main.py --demo

# 运行 pytest 测试
pytest tests/test_login.py -v --html=reports/test_report.html

# 运行 DDT 测试
python -m pytest tests/test_login_ddt.py -v

# 指定商城类型运行
SHOP_TYPE=shopxo pytest tests/test_login.py -v
```

## 📁 项目结构

### 方式一：在 TPshop 前台注册

1. 访问 TPshop 商城首页
2. 点击"注册"
3. 填写手机号 `13800138000`，密码 `123456`
4. 完成注册

### 方式二：在 TPshop 后台添加

1. 登录 TPshop 后台
2. 进入 **会员管理 → 会员列表**
3. 点击"添加会员"
4. 填写手机号和密码

### 方式三：使用环境变量

```bash
export TEST_USERNAME="你的测试账号"
export TEST_PASSWORD="你的测试密码"
```

## 项目结构

```
├── backend/
│   ├── utils/
│   │   └── driver.py           # UtilsDriver 浏览器驱动工具类
│   ├── pages/
│   │   ├── __init__.py
│   │   ├── base_page.py        # BasePage + BaseHandle 基类
│   │   ├── home_page.py        # 商城首页 PO
│   │   └── login_page.py       # 登录页面 PO
│   ├── data/
│   │   └── login_data.json     # 测试数据（DDT）
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_login.py       # pytest 参数化测试
│   │   └── test_login_ddt.py   # DDT库测试（符合实验要求）
│   ├── reports/                # 测试报告目录
│   │   └── screenshots/        # 测试截图目录
│   ├── docs/
│   │   ├── TPSHOP_DEPLOY.md    # TPshop部署指南
│   │   └── TEST_ANALYSIS.md    # 测试结果分析
│   ├── config.py               # 配置文件
│   ├── conftest.py             # pytest 配置
│   ├── main.py                 # 主程序入口
│   ├── requirements.txt
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

## 环境配置

### 1. TPshop商城部署

详见 `backend/docs/TPSHOP_DEPLOY.md`

简要步骤：
1. 使用 phpStudy 或 Docker 部署 TPshop
2. 配置万能验证码 `8888`
3. 创建测试账号

### 2. 测试环境配置

通过环境变量配置（可选）：

```bash
export TEST_URL="http://localhost:8080"    # TPshop地址
export TEST_USERNAME="13800138000"          # 测试用户名
export TEST_PASSWORD="123456"               # 测试密码
export VERIFY_CODE="8888"                   # 万能验证码
export HEADLESS="false"                     # 是否无头模式
```

## 运行测试

### 方式一：Docker 运行（演示模式）

```bash
docker compose up --build
```

### 方式二：本地运行

```bash
cd backend
pip install -r requirements.txt

# 演示模式
python main.py --demo

# 运行 pytest 测试（需要TPshop环境）
pytest tests/test_login.py -v --html=reports/test_report.html

# 运行 DDT 测试（符合实验要求）
python -m pytest tests/test_login_ddt.py -v

# 生成覆盖率报告
pytest --cov=pages --cov=utils --cov-report=html tests/
```

## PO 设计模式说明

### 1. UtilsDriver - 浏览器驱动工具类

```python
class UtilsDriver:
    """单例模式管理 WebDriver"""
    _driver = None
    
    @classmethod
    def get_driver(cls):
        """获取浏览器驱动实例"""
        if cls._driver is None:
            cls._driver = cls._init_driver()
        return cls._driver
    
    @classmethod
    def navigate_to(cls, url):
        """导航到指定URL"""
        cls.get_driver().get(url)
    
    @classmethod
    def quit_driver(cls):
        """关闭浏览器"""
        if cls._driver:
            cls._driver.quit()
            cls._driver = None
```

### 2. BasePage - 页面元素定位基类

```python
class BasePage:
    """封装各种定位方法"""
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, EXPLICIT_WAIT)
    
    def find_element_by_id(self, element_id):
        return self.wait.until(EC.presence_of_element_located((By.ID, element_id)))
    
    def find_element_by_xpath(self, xpath):
        return self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
    
    def find_element_by_name(self, name):
        return self.wait.until(EC.presence_of_element_located((By.NAME, name)))
```

### 3. BaseHandle - 页面操作处理基类

```python
class BaseHandle:
    """封装输入、点击、等待等操作"""
    def input_text(self, element, text, clear_first=True):
        if clear_first:
            element.clear()
        element.send_keys(text)
    
    def click_element(self, element, retry=3):
        for i in range(retry):
            try:
                element.click()
                return
            except Exception:
                time.sleep(0.5)
    
    def take_screenshot(self, name):
        filepath = os.path.join(SCREENSHOT_DIR, f"{name}_{timestamp}.png")
        self.driver.save_screenshot(filepath)
```

### 4. 页面对象类

- **HomePage**: 商城首页，包含登录入口、搜索框等
- **LoginPage**: 登录页面，包含用户名、密码、验证码输入框
- **LoginPageHandle**: 登录页面操作处理，封装登录业务逻辑

## DDT 数据驱动

### 测试数据 (data/login_data.json)

```json
[
  {"case_id": "TC001", "description": "正确用户名和密码登录", "username": "13800138000", "password": "123456", "verify_code": "8888", "expected": "success"},
  {"case_id": "TC002", "description": "用户名为空", "username": "", "password": "123456", "verify_code": "8888", "expected": "fail"},
  {"case_id": "TC003", "description": "密码为空", "username": "13800138000", "password": "", "verify_code": "8888", "expected": "fail"},
  {"case_id": "TC004", "description": "错误的用户名", "username": "wronguser", "password": "123456", "verify_code": "8888", "expected": "fail"},
  {"case_id": "TC005", "description": "错误的密码", "username": "13800138000", "password": "wrongpassword", "verify_code": "8888", "expected": "fail"},
  {"case_id": "TC006", "description": "验证码为空", "username": "13800138000", "password": "123456", "verify_code": "", "expected": "fail"}
]
```

### DDT库使用示例 (test_login_ddt.py)

```python
from ddt import ddt, data

@ddt
class TestLoginDDT(unittest.TestCase):
    
    @data(*load_test_data())
    def test_login(self, test_data):
        """使用DDT库的@data装饰器实现数据驱动"""
        case_id = test_data['case_id']
        username = test_data['username']
        password = test_data['password']
        # 执行测试...
```

## 验证码处理说明

TPshop商城验证码处理方案：

1. **万能验证码**: 在TPshop后台配置万能验证码 `8888`
2. **配置文件**: 通过 `config.py` 中的 `UNIVERSAL_VERIFY_CODE` 配置
3. **环境变量**: 通过 `VERIFY_CODE` 环境变量覆盖

```python
# config.py
UNIVERSAL_VERIFY_CODE = os.getenv("VERIFY_CODE", "8888")
```

## 测试报告

运行测试后，报告生成在 `backend/reports/` 目录：

- `test_report.html` - HTML格式测试报告
- `screenshots/` - 测试过程截图

## 技术栈

- Python 3.11
- Selenium 4.x
- pytest + pytest-html + pytest-cov
- DDT (Data-Driven Tests)
- WebDriver Manager
- Docker
