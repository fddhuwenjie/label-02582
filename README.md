# TPshop 商城登录功能自动化测试

基于 PO（Page Object）设计模式 + DDT 数据驱动的自动化测试框架，实现 TPshop 开源商城网站的登录功能测试。

## How to Run

```bash
# 使用 Docker 运行（推荐）
docker compose up --build

# 或本地运行
cd backend
pip install -r requirements.txt
python main.py --demo           # 演示模式
```

## Services

| 服务 | 说明 |
|------|------|
| backend | Python 自动化测试框架 |

## 测试账号

TPshop 商城测试账号（需自行注册或使用演示数据）：
- 用户名: 13800138000
- 密码: 123456

## 题目内容

一、实验目的
- 熟练掌握PO（Page Object）设计模式在自动化测试中的应用
- 通过该模式将页面元素与测试逻辑分离，提高测试代码的可读性和可维护性
- 能够独立创建工具类、基类和页面对象类
- 熟练掌握基于DDT数据驱动的实现方式，能够通过DDT读取JSON数据

二、实验原理
1. 创建工具类UtilsDriver：实现浏览器的初始化、启动和关闭
2. 创建基类BasePage与BaseHandle：BasePage定义页面元素的定位方法，BaseHandle封装公共处理逻辑
3. 商城首页的PO模式代码
4. 登录页面的PO模式代码
5. 准备测试数据，创建JSON文件
6. 创建登录功能的测试用例

---

## 测试步骤

### 1. Docker 构建与运行测试

```bash
# 进入项目目录
cd 2582

# 构建并运行
docker compose up --build
```

预期输出：
```
tpshop-test  | ============================================================
tpshop-test  | TPshop 商城登录功能自动化测试框架
tpshop-test  | 基于 PO（Page Object）设计模式 + DDT 数据驱动
tpshop-test  | ============================================================
tpshop-test  | 
tpshop-test  | 📁 项目结构:
tpshop-test  | 
tpshop-test  |     backend/
tpshop-test  |     ├── utils/
tpshop-test  |     │   └── driver.py        # 浏览器驱动工具类
tpshop-test  |     ├── pages/
tpshop-test  |     │   ├── base_page.py     # 基类 BasePage + BaseHandle
tpshop-test  |     │   ├── home_page.py     # 商城首页 PO
tpshop-test  |     │   └── login_page.py    # 登录页面 PO
...
tpshop-test  | ✅ 框架特性:
tpshop-test  |   - PO 设计模式：页面元素与测试逻辑分离
tpshop-test  |   - DDT 数据驱动：从 JSON 读取测试数据
tpshop-test  |   - pytest 框架：参数化测试、HTML 报告
tpshop-test exited with code 0
```

### 2. 功能验证

| 测试项 | 预期结果 | 实际结果 |
|--------|----------|----------|
| Docker 构建 | 成功构建镜像 | ✅ 通过 |
| 依赖安装 | selenium/pytest 安装成功 | ✅ 通过 |
| 容器启动 | 正常启动并输出 | ✅ 通过 |
| 项目结构展示 | 显示完整结构 | ✅ 通过 |
| 测试数据展示 | 显示 6 个测试用例 | ✅ 通过 |
| PO 模式说明 | 显示设计模式说明 | ✅ 通过 |
| 退出码 | code 0 | ✅ 通过 |

### 3. 实际测试运行（需要浏览器环境）

```bash
# 在有浏览器的环境中运行
cd backend
pytest tests/ -v --html=reports/test_report.html

# 或使用 headless 模式
pytest tests/ -v --headless
```

---

## 项目结构

```
2582/
├── backend/
│   ├── utils/
│   │   └── driver.py        # UtilsDriver 浏览器驱动工具类
│   ├── pages/
│   │   ├── __init__.py
│   │   ├── base_page.py     # BasePage + BaseHandle 基类
│   │   ├── home_page.py     # 商城首页 PO
│   │   └── login_page.py    # 登录页面 PO
│   ├── data/
│   │   └── login_data.json  # 测试数据（DDT）
│   ├── tests/
│   │   ├── __init__.py
│   │   └── test_login.py    # 登录测试用例
│   ├── reports/             # 测试报告目录
│   ├── config.py            # 配置文件
│   ├── conftest.py          # pytest 配置
│   ├── main.py              # 主程序入口
│   ├── requirements.txt
│   └── Dockerfile
├── docker-compose.yml
├── .gitignore
├── label-02582.md           # 轨迹文档
└── README.md
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
```

### 2. BasePage - 页面元素定位基类

```python
class BasePage:
    """封装各种定位方法"""
    def find_element_by_id(self, element_id):
        return self.wait.until(EC.presence_of_element_located((By.ID, element_id)))
    
    def find_element_by_xpath(self, xpath):
        return self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
```

### 3. BaseHandle - 页面操作处理基类

```python
class BaseHandle:
    """封装输入、点击、等待等操作"""
    def input_text(self, element, text):
        element.clear()
        element.send_keys(text)
    
    def click_element(self, element):
        element.click()
```

### 4. 页面对象类

- **HomePage**: 商城首页，包含登录入口、搜索框等
- **LoginPage**: 登录页面，包含用户名、密码、验证码输入框

## 测试数据（DDT）

`data/login_data.json`:
```json
[
  {"case_id": "TC001", "description": "正确用户名和密码登录", "username": "13800138000", "password": "123456", "expected": "success"},
  {"case_id": "TC002", "description": "用户名为空", "username": "", "password": "123456", "expected": "fail"},
  {"case_id": "TC003", "description": "密码为空", "username": "13800138000", "password": "", "expected": "fail"},
  {"case_id": "TC004", "description": "错误的用户名", "username": "wronguser", "password": "123456", "expected": "fail"},
  {"case_id": "TC005", "description": "错误的密码", "username": "13800138000", "password": "wrongpwd", "expected": "fail"},
  {"case_id": "TC006", "description": "验证码为空", "username": "13800138000", "password": "123456", "verify_code": "", "expected": "fail"}
]
```

## 技术栈

- Python 3.11
- Selenium 4.x
- pytest + pytest-html
- WebDriver Manager
- Docker
