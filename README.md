# 商城登录功能自动化测试

基于 PO（Page Object）设计模式 + DDT 数据驱动的自动化测试框架，支持多种商城系统的登录功能测试。

## ⚠️ 测试环境说明

**重要**：本项目是一个**自动化测试框架**，需要用户自行准备商城测试环境。

### 环境要求

| 组件 | 要求 |
|------|------|
| Python | 3.8+ |
| Chrome | 最新版本 |
| 商城环境 | TPshop / ShopXO / 其他 |

### 测试环境类型

1. **真实环境测试**（推荐）
   - 部署 TPshop 商城（本地）
   - 配置万能验证码
   - 创建测试账号
   - 运行完整测试用例

2. **演示模式**（无需商城）
   - 运行 `python main.py --demo`
   - 查看框架结构和设计说明
   - 不执行实际浏览器操作

## ⚠️ 关于测试截图和报告

**重要说明**：

1. **截图目录** (`reports/screenshots/`)：测试运行时自动生成，需要真实商城环境
2. **测试报告** (`reports/test_report.html`)：pytest-html 自动生成，需要运行真实测试
3. **演示模式**：`python main.py --demo` 仅展示框架结构，不执行浏览器操作

本项目是一个**自动化测试框架**，截图和报告需要在配置好商城环境后运行测试才能生成。

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

## 🐳 Docker 部署（推荐）

使用 Docker 可以快速部署测试环境，无需手动配置 Python 和 Chrome 浏览器。

### ⚠️ 重要说明：TPshop 镜像访问问题

**当前配置中的 TPshop 镜像 `registry.cn-hangzhou.aliyuncs.com/qingfeng666/tpshop:latest` 可能无法访问**。

请根据以下方案解决：

1. **方案一：使用自定义 TPshop 镜像**
   - 自行部署 TPshop 商城并构建 Docker 镜像
   - 修改 `docker-compose.yml` 中的 `image` 字段为你的镜像地址

2. **方案二：本地手动启动 TPshop**
   - 在本地手动启动 TPshop 服务（如使用 phpStudy、XAMPP 等）
   - 修改 `docker-compose.yml` 中 `TEST_URL` 为本地地址（如 `http://host.docker.internal:8080`）
   - 或使用环境变量覆盖：`-e TEST_URL=http://host.docker.internal:8080`

3. **方案三：仅运行测试框架演示模式**
   - 无需 TPshop 镜像，直接运行演示模式
   - 命令：`./docker-run.sh demo` 或 `docker compose run --rm --profile demo tpshop-demo`

### 方式一：使用启动脚本（推荐）

```bash
# 1. 构建镜像并启动服务运行测试
./docker-run.sh all

# 2. 其他常用命令
./docker-run.sh build      # 仅构建镜像
./docker-run.sh start      # 启动 TPshop Web 服务
./docker-run.sh test       # 运行自动化测试
./docker-run.sh demo       # 演示模式（查看框架结构）
./docker-run.sh logs       # 查看日志
./docker-run.sh stop       # 停止服务
./docker-run.sh clean      # 清理资源
```

### 方式二：使用 docker compose 命令

```bash
# 构建镜像
docker compose build

# 启动 TPshop Web 服务
docker compose up -d tpshop-web

# 运行自动化测试（需要Web服务已启动）
docker compose run --rm tpshop-test

# 运行演示模式
docker compose run --rm tpshop-demo

# 一键启动Web服务并运行测试
docker compose up --abort-on-container-exit

# 查看 Web 服务日志
docker compose logs -f tpshop-web

# 停止服务
docker compose down
```

### Docker 环境变量配置

可以通过环境变量自定义测试配置：

```bash
# 自定义测试地址和账号
docker-compose run -e TEST_URL=http://your-shop-url:8080 \
                   -e TEST_USERNAME=your_phone \
                   -e TEST_PASSWORD=your_password \
                   --rm tpshop-test
```

## 🚀 本地运行测试

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

# 运行 pytest 测试（需要商城环境）
pytest tests/test_login.py -v --html=reports/test_report.html

# 运行 DDT 测试
python -m pytest tests/test_login_ddt.py -v

# 指定商城类型运行
SHOP_TYPE=tpshop TEST_URL=http://localhost:8080 pytest tests/test_login.py -v
```

### 4. 查看测试报告

测试完成后，报告生成在 `reports/` 目录：
- `test_report.html` - HTML 格式测试报告
- `screenshots/` - 测试过程截图

## 📸 测试截图说明

测试运行时会自动截图保存到 `reports/screenshots/` 目录：

| 截图 | 说明 |
|------|------|
| `TC001_before_login.png` | 登录前页面 |
| `TC001_after_login.png` | 登录后页面 |
| `TC002_error.png` | 错误提示截图 |

## 📊 测试报告示例

运行测试后，打开 `reports/test_report.html` 查看：

```
============================= test session starts ==============================
platform darwin -- Python 3.9.8, pytest-8.4.2
collected 6 items

tests/test_login.py::TestLogin::test_login[TC001] PASSED
tests/test_login.py::TestLogin::test_login[TC002] PASSED
tests/test_login.py::TestLogin::test_login[TC003] PASSED
tests/test_login.py::TestLogin::test_login[TC004] PASSED
tests/test_login.py::TestLogin::test_login[TC005] PASSED
tests/test_login.py::TestLogin::test_login[TC006] PASSED

============================== 6 passed in 45.23s ==============================
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
│   └── requirements.txt        # Python依赖
├── Dockerfile                  # Docker镜像构建文件
├── docker-compose.yml          # Docker Compose编排配置
├── docker-run.sh               # Docker启动脚本
├── .gitignore                  # Git忽略配置
└── README.md                   # 项目说明文档
```

## 环境配置

### 1. TPshop商城部署

详见 `backend/docs/TPSHOP_DEPLOY.md`

简要步骤：
1. 使用 phpStudy 部署 TPshop
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

### 本地运行

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
