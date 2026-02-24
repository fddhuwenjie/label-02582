"""
主程序入口 - 运行测试
"""
import os
import sys
import pytest
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def run_tests():
    """运行所有测试"""
    logger.info("=" * 50)
    logger.info("TPshop 商城登录功能自动化测试")
    logger.info("基于 PO 设计模式 + DDT 数据驱动")
    logger.info("=" * 50)
    
    # 确保报告目录存在
    report_dir = os.path.join(os.path.dirname(__file__), "reports")
    os.makedirs(report_dir, exist_ok=True)
    
    # 运行 pytest
    args = [
        "-v",
        "-s",
        "--tb=short",
        f"--html={report_dir}/test_report.html",
        "--self-contained-html",
        os.path.join(os.path.dirname(__file__), "tests")
    ]
    
    exit_code = pytest.main(args)
    
    if exit_code == 0:
        logger.info("✓ 所有测试通过")
    else:
        logger.error(f"✗ 测试失败，退出码: {exit_code}")
    
    return exit_code


def demo_mode():
    """演示模式 - 不实际运行浏览器，展示框架结构"""
    print("=" * 60)
    print("TPshop 商城登录功能自动化测试框架")
    print("基于 PO（Page Object）设计模式 + DDT 数据驱动")
    print("=" * 60)
    
    print("\n📁 项目结构:")
    print("""
    backend/
    ├── utils/
    │   └── driver.py        # 浏览器驱动工具类
    ├── pages/
    │   ├── base_page.py     # 基类 BasePage + BaseHandle
    │   ├── home_page.py     # 商城首页 PO
    │   └── login_page.py    # 登录页面 PO
    ├── data/
    │   └── login_data.json  # 测试数据（DDT）
    ├── tests/
    │   └── test_login.py    # 登录测试用例
    ├── reports/             # 测试报告目录
    ├── config.py            # 配置文件
    ├── conftest.py          # pytest 配置
    └── main.py              # 主程序入口
    """)
    
    print("\n📋 测试数据 (login_data.json):")
    import json
    data_path = os.path.join(os.path.dirname(__file__), "data", "login_data.json")
    with open(data_path, 'r', encoding='utf-8') as f:
        test_data = json.load(f)
    for case in test_data:
        print(f"  - {case['case_id']}: {case['description']}")
    
    print("\n🔧 PO 设计模式说明:")
    print("""
    1. UtilsDriver: 浏览器驱动工具类
       - 单例模式管理 WebDriver
       - 提供导航、窗口控制等方法
    
    2. BasePage: 页面元素定位基类
       - 封装各种定位方法（ID、XPath、CSS等）
       - 使用显式等待确保元素可用
    
    3. BaseHandle: 页面操作处理基类
       - 封装输入、点击、等待等操作
       - 提供统一的操作接口
    
    4. HomePage/LoginPage: 具体页面对象
       - 继承 BasePage，定义页面特有元素
       - 对应 Handle 类封装业务操作
    """)
    
    print("\n✅ 框架特性:")
    print("  - PO 设计模式：页面元素与测试逻辑分离")
    print("  - DDT 数据驱动：从 JSON 读取测试数据")
    print("  - pytest 框架：参数化测试、HTML 报告")
    print("  - 日志记录：详细的操作日志")
    print("  - 配置管理：支持环境变量配置")


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--demo':
        demo_mode()
    else:
        print("使用 --demo 参数查看框架演示")
        print("使用 pytest 运行实际测试（需要配置测试环境）")
        demo_mode()
