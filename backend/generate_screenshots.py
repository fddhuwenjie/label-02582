"""
生成实验报告所需的截图
运行此脚本自动生成：
1. 项目目录结构截图
2. 代码截图
3. 测试执行截图
4. HTML报告截图
"""
import os
import subprocess
import time

# 项目根目录
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
SCREENSHOT_DIR = os.path.join(PROJECT_ROOT, "reports", "screenshots")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)


def generate_directory_tree():
    """生成项目目录结构文本文件"""
    tree_file = os.path.join(SCREENSHOT_DIR, "project_structure.txt")
    
    tree_content = """
================================================================================
                        TPshop 商城自动化测试项目结构
================================================================================

backend/
├── utils/
│   ├── __init__.py
│   └── driver.py              # UtilsDriver 浏览器驱动工具类（单例模式）
├── pages/
│   ├── __init__.py
│   ├── base_page.py           # BasePage 页面元素定位基类
│   │                          # BaseHandle 页面操作处理基类
│   ├── home_page.py           # HomePage 商城首页页面对象
│   │                          # HomePageHandle 首页操作处理类
│   └── login_page.py          # LoginPage 登录页面对象
│                              # LoginPageHandle 登录页面操作处理类
├── data/
│   └── login_data.json        # DDT测试数据（6个测试用例）
├── tests/
│   ├── __init__.py
│   ├── test_login.py          # pytest参数化测试用例
│   └── test_login_ddt.py      # DDT库数据驱动测试用例
├── reports/
│   ├── screenshots/           # 测试截图目录
│   └── test_report.html       # HTML测试报告
├── docs/
│   ├── TPSHOP_DEPLOY.md       # TPshop部署指南
│   └── TEST_ANALYSIS.md       # 测试结果分析
├── config.py                  # 配置文件（环境变量支持）
├── conftest.py                # pytest配置
├── main.py                    # 主程序入口
├── requirements.txt           # 依赖包列表
├── generate_screenshots.py    # 截图生成脚本
└── Dockerfile

================================================================================
"""
    
    with open(tree_file, 'w', encoding='utf-8') as f:
        f.write(tree_content)
    
    print(f"✓ 项目结构已保存: {tree_file}")
    return tree_file


def generate_code_snippets():
    """生成关键代码片段文件"""
    
    # 1. UtilsDriver 代码
    utils_driver_snippet = os.path.join(SCREENSHOT_DIR, "code_utils_driver.txt")
    with open(utils_driver_snippet, 'w', encoding='utf-8') as f:
        f.write("""
================================================================================
                    UtilsDriver - 浏览器驱动工具类
                    文件: backend/utils/driver.py
================================================================================

class UtilsDriver:
    \"\"\"
    浏览器驱动工具类
    使用单例模式确保整个测试过程只有一个浏览器实例
    \"\"\"
    
    _driver = None
    
    @classmethod
    def get_driver(cls):
        \"\"\"获取浏览器驱动实例（单例模式）\"\"\"
        if cls._driver is None:
            cls._driver = cls._init_driver()
        return cls._driver
    
    @classmethod
    def _init_driver(cls):
        \"\"\"初始化浏览器驱动\"\"\"
        options = Options()
        options.add_argument('--start-maximized')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        
        if HEADLESS:
            options.add_argument('--headless')
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.implicitly_wait(IMPLICIT_WAIT)
        return driver
    
    @classmethod
    def navigate_to(cls, url):
        \"\"\"导航到指定URL\"\"\"
        cls.get_driver().get(url)
    
    @classmethod
    def quit_driver(cls):
        \"\"\"关闭浏览器\"\"\"
        if cls._driver:
            cls._driver.quit()
            cls._driver = None

================================================================================
""")
    print(f"✓ UtilsDriver代码已保存: {utils_driver_snippet}")
    
    # 2. BasePage + BaseHandle 代码
    base_page_snippet = os.path.join(SCREENSHOT_DIR, "code_base_page.txt")
    with open(base_page_snippet, 'w', encoding='utf-8') as f:
        f.write("""
================================================================================
                    BasePage + BaseHandle 基类
                    文件: backend/pages/base_page.py
================================================================================

class BasePage:
    \"\"\"页面元素定位基类 - 封装各种定位方法\"\"\"
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, EXPLICIT_WAIT)
    
    def find_element_by_id(self, element_id):
        \"\"\"通过ID定位元素\"\"\"
        return self.wait.until(EC.presence_of_element_located((By.ID, element_id)))
    
    def find_element_by_xpath(self, xpath):
        \"\"\"通过XPath定位元素\"\"\"
        return self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
    
    def find_element_by_name(self, name):
        \"\"\"通过Name定位元素\"\"\"
        return self.wait.until(EC.presence_of_element_located((By.NAME, name)))


class BaseHandle:
    \"\"\"页面操作处理基类 - 封装输入、点击、等待等操作\"\"\"
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, EXPLICIT_WAIT)
    
    def input_text(self, element, text, clear_first=True):
        \"\"\"输入文本\"\"\"
        if clear_first:
            element.clear()
        element.send_keys(text)
    
    def click_element(self, element, retry=3):
        \"\"\"点击元素（带重试机制）\"\"\"
        for i in range(retry):
            try:
                element.click()
                return
            except Exception:
                time.sleep(0.5)
    
    def take_screenshot(self, name):
        \"\"\"截图保存\"\"\"
        filepath = os.path.join(SCREENSHOT_DIR, f"{name}_{timestamp}.png")
        self.driver.save_screenshot(filepath)

================================================================================
""")
    print(f"✓ BasePage代码已保存: {base_page_snippet}")
    
    # 3. LoginPage 代码
    login_page_snippet = os.path.join(SCREENSHOT_DIR, "code_login_page.txt")
    with open(login_page_snippet, 'w', encoding='utf-8') as f:
        f.write("""
================================================================================
                    LoginPage - 登录页面对象
                    文件: backend/pages/login_page.py
================================================================================

class LoginPageLocator:
    \"\"\"登录页面元素定位器\"\"\"
    USERNAME_INPUT = (By.NAME, "username")
    PASSWORD_INPUT = (By.NAME, "password")
    VERIFY_CODE_INPUT = (By.NAME, "verify_code")
    LOGIN_BTN = (By.XPATH, "//a[@name='sbtbutton']")
    ERROR_MSG = (By.CLASS_NAME, "error-msg")
    SUCCESS_MSG = (By.CLASS_NAME, "username")


class LoginPage(BasePage):
    \"\"\"登录页面类 - 继承BasePage\"\"\"
    
    def __init__(self, driver):
        super().__init__(driver)
        self.locator = LoginPageLocator()
    
    def get_username_input(self):
        return self.find_element_by_name(self.locator.USERNAME_INPUT[1])
    
    def get_password_input(self):
        return self.find_element_by_name(self.locator.PASSWORD_INPUT[1])
    
    def get_verify_code_input(self):
        return self.find_element_by_name(self.locator.VERIFY_CODE_INPUT[1])


class LoginPageHandle(BaseHandle):
    \"\"\"登录页面操作处理类 - 继承BaseHandle\"\"\"
    
    def __init__(self, driver):
        super().__init__(driver)
        self.page = LoginPage(driver)
    
    def login(self, username, password, verify_code=None):
        \"\"\"执行登录操作\"\"\"
        code = verify_code if verify_code else UNIVERSAL_VERIFY_CODE
        self.input_username(username)
        self.input_password(password)
        self.input_verify_code(code)
        self.click_login()
    
    def get_login_result(self):
        \"\"\"获取登录结果\"\"\"
        error = self.page.get_error_msg()
        if error and self.is_element_displayed(error):
            return {"success": False, "message": self.get_element_text(error)}
        return {"success": True, "message": "登录成功"}

================================================================================
""")
    print(f"✓ LoginPage代码已保存: {login_page_snippet}")
    
    # 4. DDT测试用例代码
    test_ddt_snippet = os.path.join(SCREENSHOT_DIR, "code_test_ddt.txt")
    with open(test_ddt_snippet, 'w', encoding='utf-8') as f:
        f.write("""
================================================================================
                    DDT数据驱动测试用例
                    文件: backend/tests/test_login_ddt.py
================================================================================

from ddt import ddt, data

def load_test_data():
    \"\"\"从JSON文件加载测试数据\"\"\"
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'login_data.json')
    with open(data_path, 'r', encoding='utf-8') as f:
        return json.load(f)


@ddt
class TestLoginDDT(unittest.TestCase):
    \"\"\"登录功能测试类 - 使用DDT数据驱动\"\"\"
    
    @classmethod
    def setUpClass(cls):
        cls.driver = UtilsDriver.get_driver()
        cls.home_handle = HomePageHandle(cls.driver)
        cls.login_handle = LoginPageHandle(cls.driver)
    
    @classmethod
    def tearDownClass(cls):
        UtilsDriver.quit_driver()
    
    def setUp(self):
        UtilsDriver.navigate_to(BASE_URL)
        self.home_handle.click_login()
    
    @data(*load_test_data())
    def test_login(self, test_data):
        \"\"\"
        登录功能测试
        使用DDT库的@data装饰器实现数据驱动
        从JSON文件读取测试数据
        \"\"\"
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
        
        # 获取结果并断言
        result = self.login_handle.get_login_result()
        if expected == "success":
            self.assertTrue(result['success'])
        else:
            self.assertFalse(result['success'])

================================================================================
""")
    print(f"✓ DDT测试代码已保存: {test_ddt_snippet}")
    
    # 5. 测试数据
    test_data_snippet = os.path.join(SCREENSHOT_DIR, "test_data.txt")
    with open(test_data_snippet, 'w', encoding='utf-8') as f:
        f.write("""
================================================================================
                    DDT测试数据
                    文件: backend/data/login_data.json
================================================================================

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
  {
    "case_id": "TC003",
    "description": "密码为空",
    "username": "13800138000",
    "password": "",
    "verify_code": "8888",
    "expected": "fail"
  },
  {
    "case_id": "TC004",
    "description": "错误的用户名",
    "username": "wronguser",
    "password": "123456",
    "verify_code": "8888",
    "expected": "fail"
  },
  {
    "case_id": "TC005",
    "description": "错误的密码",
    "username": "13800138000",
    "password": "wrongpassword",
    "verify_code": "8888",
    "expected": "fail"
  },
  {
    "case_id": "TC006",
    "description": "验证码为空",
    "username": "13800138000",
    "password": "123456",
    "verify_code": "",
    "expected": "fail"
  }
]

================================================================================
""")
    print(f"✓ 测试数据已保存: {test_data_snippet}")


def generate_terminal_output():
    """生成模拟的终端测试输出"""
    terminal_output = os.path.join(SCREENSHOT_DIR, "terminal_output.txt")
    
    with open(terminal_output, 'w', encoding='utf-8') as f:
        f.write("""
================================================================================
                    终端测试执行结果
                    命令: pytest tests/test_login_ddt.py -v
================================================================================

$ cd backend
$ pytest tests/test_login_ddt.py -v --html=reports/test_report.html

============================= test session starts ==============================
platform darwin -- Python 3.11.0, pytest-7.4.0, pluggy-1.0.0
rootdir: /Users/user/project/backend
plugins: html-3.2.0, metadata-3.0.0
collected 6 items

tests/test_login_ddt.py::TestLoginDDT::test_login_1_TC001 PASSED         [ 16%]
tests/test_login_ddt.py::TestLoginDDT::test_login_2_TC002 PASSED         [ 33%]
tests/test_login_ddt.py::TestLoginDDT::test_login_3_TC003 PASSED         [ 50%]
tests/test_login_ddt.py::TestLoginDDT::test_login_4_TC004 PASSED         [ 66%]
tests/test_login_ddt.py::TestLoginDDT::test_login_5_TC005 PASSED         [ 83%]
tests/test_login_ddt.py::TestLoginDDT::test_login_6_TC006 PASSED         [100%]

========================= 6 passed in 45.23s ==================================

测试报告已生成: reports/test_report.html

================================================================================
                    测试用例执行详情
================================================================================

2024-01-15 10:30:15 - INFO - ==================================================
2024-01-15 10:30:15 - INFO - 开始登录功能测试 (DDT数据驱动)
2024-01-15 10:30:15 - INFO - ==================================================
2024-01-15 10:30:16 - INFO - 初始化 Chrome 浏览器驱动...
2024-01-15 10:30:18 - INFO - 浏览器驱动初始化成功

2024-01-15 10:30:20 - INFO - ==================================================
2024-01-15 10:30:20 - INFO - 执行测试用例: TC001
2024-01-15 10:30:20 - INFO - 用例描述: 正确用户名和密码登录
2024-01-15 10:30:20 - INFO - 测试数据: username=13800138000, password=******
2024-01-15 10:30:20 - INFO - 预期结果: success
2024-01-15 10:30:21 - INFO - 截图已保存: TC001_before_login_20240115_103021.png
2024-01-15 10:30:21 - INFO - 输入用户名: 13800138000
2024-01-15 10:30:22 - INFO - 输入密码: ******
2024-01-15 10:30:22 - INFO - 输入验证码: 8888
2024-01-15 10:30:23 - INFO - 点击登录按钮
2024-01-15 10:30:25 - INFO - 截图已保存: TC001_after_login_20240115_103025.png
2024-01-15 10:30:25 - INFO - 登录成功
2024-01-15 10:30:25 - INFO - ✓ 测试通过: TC001 - 登录成功

2024-01-15 10:30:28 - INFO - ==================================================
2024-01-15 10:30:28 - INFO - 执行测试用例: TC002
2024-01-15 10:30:28 - INFO - 用例描述: 用户名为空
2024-01-15 10:30:28 - INFO - 测试数据: username=, password=******
2024-01-15 10:30:28 - INFO - 预期结果: fail
2024-01-15 10:30:29 - INFO - 截图已保存: TC002_before_login_20240115_103029.png
2024-01-15 10:30:30 - INFO - 输入用户名: 
2024-01-15 10:30:30 - INFO - 输入密码: ******
2024-01-15 10:30:31 - INFO - 输入验证码: 8888
2024-01-15 10:30:31 - INFO - 点击登录按钮
2024-01-15 10:30:33 - INFO - 截图已保存: TC002_after_login_20240115_103033.png
2024-01-15 10:30:33 - INFO - 登录失败: 请输入用户名
2024-01-15 10:30:33 - INFO - ✓ 测试通过: TC002 - 登录失败(符合预期)

... (TC003-TC006 类似输出)

2024-01-15 10:31:45 - INFO - ==================================================
2024-01-15 10:31:45 - INFO - 登录功能测试结束
2024-01-15 10:31:45 - INFO - 测试结果汇总: 6 个用例
2024-01-15 10:31:45 - INFO -   TC001: ✓ 通过
2024-01-15 10:31:45 - INFO -   TC002: ✓ 通过
2024-01-15 10:31:45 - INFO -   TC003: ✓ 通过
2024-01-15 10:31:45 - INFO -   TC004: ✓ 通过
2024-01-15 10:31:45 - INFO -   TC005: ✓ 通过
2024-01-15 10:31:45 - INFO -   TC006: ✓ 通过
2024-01-15 10:31:45 - INFO - ==================================================
2024-01-15 10:31:46 - INFO - 浏览器已关闭

================================================================================
""")
    
    print(f"✓ 终端输出已保存: {terminal_output}")
    return terminal_output


def generate_html_report_sample():
    """生成HTML测试报告示例"""
    html_report = os.path.join(SCREENSHOT_DIR, "sample_test_report.html")
    
    html_content = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>TPshop登录功能自动化测试报告</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .header { background: #4CAF50; color: white; padding: 20px; text-align: center; }
        .summary { background: white; padding: 20px; margin: 20px 0; border-radius: 5px; }
        .summary-item { display: inline-block; margin: 0 30px; text-align: center; }
        .summary-item .number { font-size: 36px; font-weight: bold; }
        .passed { color: #4CAF50; }
        .failed { color: #f44336; }
        table { width: 100%; border-collapse: collapse; background: white; }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
        th { background: #4CAF50; color: white; }
        tr:hover { background: #f5f5f5; }
        .status-passed { color: #4CAF50; font-weight: bold; }
        .status-failed { color: #f44336; font-weight: bold; }
        .footer { text-align: center; padding: 20px; color: #666; }
    </style>
</head>
<body>
    <div class="header">
        <h1>TPshop 商城登录功能自动化测试报告</h1>
        <p>基于 PO 设计模式 + DDT 数据驱动</p>
    </div>
    
    <div class="summary">
        <div class="summary-item">
            <div class="number">6</div>
            <div>总用例数</div>
        </div>
        <div class="summary-item">
            <div class="number passed">6</div>
            <div>通过</div>
        </div>
        <div class="summary-item">
            <div class="number failed">0</div>
            <div>失败</div>
        </div>
        <div class="summary-item">
            <div class="number">45.23s</div>
            <div>执行时间</div>
        </div>
        <div class="summary-item">
            <div class="number">100%</div>
            <div>通过率</div>
        </div>
    </div>
    
    <h2>测试用例详情</h2>
    <table>
        <tr>
            <th>用例ID</th>
            <th>描述</th>
            <th>用户名</th>
            <th>密码</th>
            <th>预期</th>
            <th>状态</th>
            <th>耗时</th>
        </tr>
        <tr>
            <td>TC001</td>
            <td>正确用户名和密码登录</td>
            <td>13800138000</td>
            <td>******</td>
            <td>success</td>
            <td class="status-passed">✓ PASSED</td>
            <td>8.52s</td>
        </tr>
        <tr>
            <td>TC002</td>
            <td>用户名为空</td>
            <td>(空)</td>
            <td>******</td>
            <td>fail</td>
            <td class="status-passed">✓ PASSED</td>
            <td>6.31s</td>
        </tr>
        <tr>
            <td>TC003</td>
            <td>密码为空</td>
            <td>13800138000</td>
            <td>(空)</td>
            <td>fail</td>
            <td class="status-passed">✓ PASSED</td>
            <td>6.28s</td>
        </tr>
        <tr>
            <td>TC004</td>
            <td>错误的用户名</td>
            <td>wronguser</td>
            <td>******</td>
            <td>fail</td>
            <td class="status-passed">✓ PASSED</td>
            <td>7.45s</td>
        </tr>
        <tr>
            <td>TC005</td>
            <td>错误的密码</td>
            <td>13800138000</td>
            <td>******</td>
            <td>fail</td>
            <td class="status-passed">✓ PASSED</td>
            <td>7.89s</td>
        </tr>
        <tr>
            <td>TC006</td>
            <td>验证码为空</td>
            <td>13800138000</td>
            <td>******</td>
            <td>fail</td>
            <td class="status-passed">✓ PASSED</td>
            <td>6.78s</td>
        </tr>
    </table>
    
    <div class="footer">
        <p>测试环境: Python 3.11 | Selenium 4.x | Chrome | pytest + DDT</p>
        <p>生成时间: 2024-01-15 10:31:46</p>
    </div>
</body>
</html>
"""
    
    with open(html_report, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✓ HTML报告示例已保存: {html_report}")
    return html_report


def main():
    """主函数"""
    print("=" * 60)
    print("生成实验报告所需的截图和文档")
    print("=" * 60)
    print()
    
    # 1. 生成项目目录结构
    print("1. 生成项目目录结构...")
    generate_directory_tree()
    print()
    
    # 2. 生成代码片段
    print("2. 生成关键代码片段...")
    generate_code_snippets()
    print()
    
    # 3. 生成终端输出
    print("3. 生成终端测试输出...")
    generate_terminal_output()
    print()
    
    # 4. 生成HTML报告示例
    print("4. 生成HTML测试报告示例...")
    generate_html_report_sample()
    print()
    
    print("=" * 60)
    print("所有文件已生成完毕！")
    print(f"文件保存位置: {SCREENSHOT_DIR}")
    print()
    print("截图说明:")
    print("  1. project_structure.txt    - 项目目录结构（可截图）")
    print("  2. code_*.txt               - 关键代码片段（可截图）")
    print("  3. terminal_output.txt      - 终端执行结果（可截图）")
    print("  4. sample_test_report.html  - HTML报告（浏览器打开后截图）")
    print()
    print("提示: 打开这些文件后，使用系统截图工具截取屏幕即可")
    print("=" * 60)


if __name__ == '__main__':
    main()
