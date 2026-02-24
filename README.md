# TPshop 商城登录功能自动化测试

基于 PO（Page Object）设计模式和 DDT 数据驱动的自动化测试框架。

## How to Run

```bash
# 进入项目目录
cd backend

# 安装依赖
pip install -r requirements.txt

# 运行演示（查看框架结构）
python main.py --demo

# 运行测试（需要配置测试环境）
pytest tests/ -v --html=reports/test_report.html
```

## 功能特性

- ✅ PO 设计模式：页面元素与测试逻辑分离
- ✅ DDT 数据驱动：从 JSON 文件读取测试数据
- ✅ pytest 框架：参数化测试、HTML 报告生成
- ✅ 工具类封装：浏览器驱动管理
- ✅ 基类设计：BasePage + BaseHandle
- ✅ 日志记录：详细的操作日志

## 项目结构

```
2582/
├── backend/
│   ├── utils/
│   │   ├── __init__.py
│   │   └── driver.py        # UtilsDriver 浏览器驱动工具类
│   ├── pages/
│   │   ├── __init__.py
│   │   ├── base_page.py     # BasePage + BaseHandle 基类
│   │   ├── home_page.py     # 商城首页页面对象
│   │   └── login_page.py    # 登录页面页面对象
│   ├── data/
│   │   └── login_data.json  # 测试数据（DDT）
│   ├── tests/
│   │   ├── __init__.py
│   │   └── test_login.py    # 登录功能测试用例
│   ├── reports/             # 测试报告目录
│   ├── config.py            # 配置文件
│   ├── conftest.py          # pytest 配置
│   ├── main.py              # 主程序入口
│   └── requirements.txt
├── docker-compose.yml
├── .gitignore
└── README.md
```

## PO 设计模式说明

### 1. UtilsDriver（工具类）

```python
from utils.driver import UtilsDriver

# 获取浏览器驱动
driver = UtilsDriver.get_driver()

# 导航到 URL
UtilsDriver.navigate_to("http://example.com")

# 关闭浏览器
UtilsDriver.quit_driver()
```

### 2. BasePage + BaseHandle（基类）

```python
class BasePage:
    """页面元素定位基类"""
    def find_element_by_id(self, element_id): ...
    def find_element_by_xpath(self, xpath): ...
    def find_element_by_css(self, css_selector): ...

class BaseHandle:
    """页面操作处理基类"""
    def input_text(self, element, text): ...
    def click_element(self, element): ...
    def wait_element_visible(self, locator): ...
```

### 3. 页面对象类

```python
class LoginPage(BasePage):
    """登录页面"""
    def get_username_input(self): ...
    def get_password_input(self): ...
    def get_login_btn(self): ...

class LoginPageHandle(BaseHandle):
    """登录页面操作"""
    def login(self, username, password, verify_code): ...
    def get_login_result(self): ...
```

## DDT 数据驱动

测试数据存储在 `data/login_data.json`：

```json
[
  {"case_id": "TC001", "description": "正确用户名和密码登录", "expected": "success"},
  {"case_id": "TC002", "description": "用户名为空", "expected": "fail"},
  {"case_id": "TC003", "description": "密码为空", "expected": "fail"}
]
```

使用 pytest 参数化：

```python
@pytest.mark.parametrize("test_data", load_test_data(), ids=lambda x: x['case_id'])
def test_login(self, test_data):
    # 执行测试
    ...
```

## 测试用例

| 用例ID | 描述 | 预期结果 |
|--------|------|----------|
| TC001 | 正确用户名和密码登录 | 成功 |
| TC002 | 用户名为空 | 失败 |
| TC003 | 密码为空 | 失败 |
| TC004 | 错误的用户名 | 失败 |
| TC005 | 错误的密码 | 失败 |
| TC006 | 验证码为空 | 失败 |

## 配置说明

通过环境变量配置：

```bash
export TEST_URL=http://localhost:8080  # 测试网站地址
export BROWSER=chrome                   # 浏览器类型
export HEADLESS=true                    # 无头模式
```
