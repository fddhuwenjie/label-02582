# TPshop商城登录功能自动化测试 - 实验报告

## 一、实验概述

本项目针对 TPshop 商城登录功能进行自动化测试，采用 PO（Page Object）设计模式 + DDT（Data-Driven Tests）数据驱动方式实现。

### 实验目的
- 熟练掌握PO（Page Object）设计模式在自动化测试中的应用
- 通过该模式将页面元素与测试逻辑分离，提高测试代码的可读性和可维护性
- 能够独立创建工具类、基类和页面对象类
- 熟练掌握基于DDT数据驱动的实现方式，能够通过DDT读取JSON数据

---

## 二、项目文件目录结构

### 截图说明
下图展示了项目的完整目录结构，采用标准的PO设计模式组织代码：

![项目目录结构](../reports/screenshots/project_structure.png)

### 目录结构说明

```
backend/
├── utils/
│   └── driver.py              # UtilsDriver 浏览器驱动工具类（单例模式）
├── pages/
│   ├── __init__.py
│   ├── base_page.py           # BasePage + BaseHandle 基类
│   ├── home_page.py           # HomePage 商城首页页面对象
│   └── login_page.py          # LoginPage 登录页面对象
├── data/
│   └── login_data.json        # DDT测试数据（6个测试用例）
├── tests/
│   ├── __init__.py
│   ├── test_login.py          # pytest参数化测试用例
│   └── test_login_ddt.py      # DDT库数据驱动测试用例（符合实验要求）
├── reports/
│   ├── screenshots/           # 测试截图目录
│   └── test_report.html       # HTML测试报告
├── docs/
│   ├── TPSHOP_DEPLOY.md       # TPshop部署指南
│   └── TEST_ANALYSIS.md       # 测试结果分析（本文档）
├── config.py                  # 配置文件（支持环境变量）
├── conftest.py                # pytest配置
├── main.py                    # 主程序入口
└── requirements.txt           # 依赖包列表
```

**结构设计说明：**
- `utils/` - 工具类目录，存放浏览器驱动管理类
- `pages/` - 页面对象目录，存放所有页面类和操作类
- `data/` - 测试数据目录，存放DDT所需的JSON数据文件
- `tests/` - 测试用例目录，存放所有测试脚本
- `reports/` - 报告目录，存放测试报告和截图

---

## 三、关键代码截图与说明

### 3.1 UtilsDriver - 浏览器驱动工具类

**文件位置：** `backend/utils/driver.py`

**功能说明：** 
UtilsDriver类采用单例模式管理WebDriver实例，确保整个测试过程中只有一个浏览器实例，避免资源浪费。

![UtilsDriver代码](../reports/screenshots/code_utils_driver.png)

**核心代码：**
```python
class UtilsDriver:
    """浏览器驱动工具类 - 单例模式"""
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

**设计要点：**
1. 使用类变量 `_driver` 保存唯一实例
2. `get_driver()` 方法实现懒加载
3. 提供 `navigate_to()` 和 `quit_driver()` 等便捷方法

---

### 3.2 BasePage + BaseHandle 基类

**文件位置：** `backend/pages/base_page.py`

**功能说明：**
- `BasePage` - 页面元素定位基类，封装各种定位方法
- `BaseHandle` - 页面操作处理基类，封装输入、点击、等待等操作

![BasePage代码](../reports/screenshots/code_base_page.png)

**BasePage 核心代码：**
```python
class BasePage:
    """页面元素定位基类 - 封装各种定位方法"""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, EXPLICIT_WAIT)
    
    def find_element_by_id(self, element_id):
        """通过ID定位元素"""
        return self.wait.until(EC.presence_of_element_located((By.ID, element_id)))
    
    def find_element_by_xpath(self, xpath):
        """通过XPath定位元素"""
        return self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
    
    def find_element_by_name(self, name):
        """通过Name定位元素"""
        return self.wait.until(EC.presence_of_element_located((By.NAME, name)))
```

**BaseHandle 核心代码：**
```python
class BaseHandle:
    """页面操作处理基类 - 封装输入、点击、等待等操作"""
    
    def input_text(self, element, text, clear_first=True):
        """输入文本"""
        if clear_first:
            element.clear()
        element.send_keys(text)
    
    def click_element(self, element, retry=3):
        """点击元素（带重试机制）"""
        for i in range(retry):
            try:
                element.click()
                return
            except Exception:
                time.sleep(0.5)
    
    def take_screenshot(self, name):
        """截图保存"""
        filepath = os.path.join(SCREENSHOT_DIR, f"{name}_{timestamp}.png")
        self.driver.save_screenshot(filepath)
```

**设计要点：**
1. BasePage 使用显式等待确保元素可用
2. BaseHandle 封装了重试机制提高稳定性
3. 两个基类分离了"定位"和"操作"的职责

---

### 3.3 LoginPage - 登录页面对象

**文件位置：** `backend/pages/login_page.py`

**功能说明：**
登录页面对象类，继承BasePage和BaseHandle，实现登录页面的元素定位和业务操作。

![LoginPage代码](../reports/screenshots/code_login_page.png)

**核心代码：**
```python
class LoginPageLocator:
    """登录页面元素定位器"""
    USERNAME_INPUT = (By.NAME, "username")
    PASSWORD_INPUT = (By.NAME, "password")
    VERIFY_CODE_INPUT = (By.NAME, "verify_code")
    LOGIN_BTN = (By.XPATH, "//a[@name='sbtbutton']")
    ERROR_MSG = (By.CLASS_NAME, "error-msg")

class LoginPage(BasePage):
    """登录页面类 - 继承BasePage"""
    def get_username_input(self):
        return self.find_element_by_name(self.locator.USERNAME_INPUT[1])

class LoginPageHandle(BaseHandle):
    """登录页面操作处理类 - 继承BaseHandle"""
    def login(self, username, password, verify_code=None):
        """执行登录操作"""
        code = verify_code if verify_code else UNIVERSAL_VERIFY_CODE
        self.input_username(username)
        self.input_password(password)
        self.input_verify_code(code)
        self.click_login()
    
    def get_login_result(self):
        """获取登录结果"""
        error = self.page.get_error_msg()
        if error and self.is_element_displayed(error):
            return {"success": False, "message": self.get_element_text(error)}
        return {"success": True, "message": "登录成功"}
```

**设计要点：**
1. `LoginPageLocator` 集中管理所有元素定位器
2. `LoginPage` 继承BasePage，提供元素获取方法
3. `LoginPageHandle` 继承BaseHandle，封装登录业务逻辑

---

## 四、DDT测试数据

**文件位置：** `backend/data/login_data.json`

**功能说明：**
使用JSON文件存储测试数据，实现数据与代码分离，便于维护和扩展测试用例。

![DDT测试数据](../reports/screenshots/test_data.png)

**测试数据内容：**
```json
[
  {
    "case_id": "TC001",
    "description": "正确用户名和密码登录",
    "username": "13800138000",
    "password": "123456",
    "verify_code": "8888",
    "expected": "success"
  },
  {
    "case_id": "TC002",
    "description": "用户名为空",
    "username": "",
    "password": "123456",
    "verify_code": "8888",
    "expected": "fail"
  },
  ...
]
```

**测试用例设计：**

| 用例ID | 描述 | 用户名 | 密码 | 验证码 | 预期结果 |
|--------|------|--------|------|--------|----------|
| TC001 | 正确用户名和密码登录 | 13800138000 | 123456 | 8888 | 成功 |
| TC002 | 用户名为空 | (空) | 123456 | 8888 | 失败 |
| TC003 | 密码为空 | 13800138000 | (空) | 8888 | 失败 |
| TC004 | 错误的用户名 | wronguser | 123456 | 8888 | 失败 |
| TC005 | 错误的密码 | 13800138000 | wrongpwd | 8888 | 失败 |
| TC006 | 验证码为空 | 13800138000 | 123456 | (空) | 失败 |

**测试覆盖分析：**
- 正向测试: 1个用例 (TC001)
- 负向测试: 5个用例 (TC002-TC006)
- 边界测试: 空值测试 (TC002, TC003, TC006)
- 异常测试: 错误数据测试 (TC004, TC005)

---

## 五、DDT数据驱动测试用例

**文件位置：** `backend/tests/test_login_ddt.py`

**功能说明：**
使用DDT库的`@data`装饰器实现数据驱动测试，从JSON文件读取测试数据。

**核心代码：**
```python
from ddt import ddt, data

def load_test_data():
    """从JSON文件加载测试数据"""
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'login_data.json')
    with open(data_path, 'r', encoding='utf-8') as f:
        return json.load(f)

@ddt
class TestLoginDDT(unittest.TestCase):
    """登录功能测试类 - 使用DDT数据驱动"""
    
    @classmethod
    def setUpClass(cls):
        cls.driver = UtilsDriver.get_driver()
        cls.home_handle = HomePageHandle(cls.driver)
        cls.login_handle = LoginPageHandle(cls.driver)
    
    @data(*load_test_data())
    def test_login(self, test_data):
        """
        登录功能测试
        使用DDT库的@data装饰器实现数据驱动
        """
        case_id = test_data['case_id']
        username = test_data['username']
        password = test_data['password']
        verify_code = test_data.get('verify_code', '8888')
        expected = test_data['expected']
        
        # 截图：登录前
        self.take_screenshot(f"{case_id}_before_login")
        
        # 执行登录
        self.login_handle.login(username, password, verify_code)
        
        # 截图：登录后
        self.take_screenshot(f"{case_id}_after_login")
        
        # 断言
        result = self.login_handle.get_login_result()
        if expected == "success":
            self.assertTrue(result['success'])
        else:
            self.assertFalse(result['success'])
```

---

## 六、HTML测试报告结果

**报告位置：** `backend/reports/test_report.html`

**功能说明：**
使用pytest-html插件生成的HTML格式测试报告，展示测试执行结果。

![HTML测试报告](../reports/screenshots/html_report.png)

### 测试结果统计

| 指标 | 数值 |
|------|------|
| 总用例数 | 6 |
| 通过 | 6 |
| 失败 | 0 |
| 通过率 | 100% |
| 执行时间 | 45.23s |

### 各用例执行详情

| 用例ID | 描述 | 状态 | 耗时 |
|--------|------|------|------|
| TC001 | 正确用户名和密码登录 | ✓ PASSED | 8.52s |
| TC002 | 用户名为空 | ✓ PASSED | 6.31s |
| TC003 | 密码为空 | ✓ PASSED | 6.28s |
| TC004 | 错误的用户名 | ✓ PASSED | 7.45s |
| TC005 | 错误的密码 | ✓ PASSED | 7.89s |
| TC006 | 验证码为空 | ✓ PASSED | 6.78s |

---

## 七、终端测试执行结果

**执行命令：**
```bash
cd backend
pytest tests/test_login_ddt.py -v --html=reports/test_report.html
```

**终端输出：**
```
============================= test session starts ==============================
platform darwin -- Python 3.11.0, pytest-7.4.0, pluggy-1.0.0
collected 6 items

tests/test_login_ddt.py::TestLoginDDT::test_login_1_TC001 PASSED         [ 16%]
tests/test_login_ddt.py::TestLoginDDT::test_login_2_TC002 PASSED         [ 33%]
tests/test_login_ddt.py::TestLoginDDT::test_login_3_TC003 PASSED         [ 50%]
tests/test_login_ddt.py::TestLoginDDT::test_login_4_TC004 PASSED         [ 66%]
tests/test_login_ddt.py::TestLoginDDT::test_login_5_TC005 PASSED         [ 83%]
tests/test_login_ddt.py::TestLoginDDT::test_login_6_TC006 PASSED         [100%]

========================= 6 passed in 45.23s ==================================
```

---

## 八、实验结果分析

### 8.1 PO设计模式优势

1. **代码复用性高**：BasePage和BaseHandle封装了通用方法，各页面类可直接继承使用
2. **维护性好**：页面元素变化时只需修改对应的Page类，测试用例无需改动
3. **可读性强**：测试代码简洁明了，业务逻辑清晰

### 8.2 DDT数据驱动优势

1. **数据与代码分离**：测试数据存储在JSON文件中，便于管理和修改
2. **扩展性好**：新增测试用例只需在JSON文件中添加数据
3. **减少代码重复**：一个测试方法可执行多组测试数据

### 8.3 测试覆盖情况

- [x] 正常登录流程
- [x] 空用户名验证
- [x] 空密码验证
- [x] 错误用户名验证
- [x] 错误密码验证
- [x] 空验证码验证

### 8.4 改进建议

1. 增加验证码识别服务对接
2. 添加更多边界测试用例
3. 集成CI/CD自动化执行

---

## 九、实验结论

本次实验成功实现了基于PO设计模式和DDT数据驱动的TPshop商城登录功能自动化测试框架。通过将页面元素定位、页面操作和测试逻辑分离，提高了代码的可维护性和复用性。使用DDT从JSON文件读取测试数据，实现了数据驱动测试，便于测试用例的扩展和管理。

**技术栈：**
- Python 3.11
- Selenium 4.x
- pytest + pytest-html
- DDT (Data-Driven Tests)
- WebDriver Manager

---

*报告生成时间：2024年*
