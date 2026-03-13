"""
主程序入口 - 运行测试
"""
import os
import sys
import pytest
import logging
import argparse

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def run_tests(test_file=None, report_name="test_report.html"):
    """运行测试"""
    logger.info("=" * 50)
    logger.info("商城登录功能自动化测试")
    logger.info("基于 PO 设计模式 + DDT 数据驱动")
    logger.info("=" * 50)
    
    # 确保报告目录存在
    report_dir = os.path.join(os.path.dirname(__file__), "reports")
    os.makedirs(report_dir, exist_ok=True)
    
    # 确定测试文件或目录
    if test_file:
        test_path = os.path.join(os.path.dirname(__file__), test_file)
    else:
        test_path = os.path.join(os.path.dirname(__file__), "tests")
    
    # 运行 pytest
    args = [
        "-v",
        "-s",
        "--tb=short",
        f"--html={report_dir}/{report_name}",
        "--self-contained-html",
        test_path
    ]
    
    logger.info(f"运行测试命令: pytest {' '.join(args)}")
    exit_code = pytest.main(args)
    
    if exit_code == 0:
        logger.info("✓ 所有测试通过")
    else:
        logger.error(f"✗ 测试失败，退出码: {exit_code}")
    
    return exit_code


def run_ddt_tests():
    """运行DDT测试"""
    return run_tests("tests/test_login_ddt.py", "ddt_test_report.html")


def run_pytest_tests():
    """运行pytest参数化测试"""
    return run_tests("tests/test_login.py", "pytest_test_report.html")


def demo_mode():
    """演示模式 - 不实际运行浏览器，展示框架结构"""
    print("=" * 60)
    print("商城登录功能自动化测试框架")
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
    │   ├── test_login.py    # pytest参数化测试
    │   └── test_login_ddt.py # DDT库测试
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
       - 支持本地Chrome和远程Selenium
       - Docker环境自动适配
    
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
    print("  - Docker 支持：一键部署和运行")
    
    # 显示当前配置
    from config import BASE_URL, HEADLESS
    print(f"\n⚙️ 当前配置:")
    print(f"  - TEST_URL: {BASE_URL}")
    print(f"  - HEADLESS: {HEADLESS}")
    print(f"  - SHOP_TYPE: {os.getenv('SHOP_TYPE', 'tpshop')}")


def check_chrome():
    """检查Chrome浏览器是否可用"""
    try:
        from utils.driver import UtilsDriver
        logger.info("检查Chrome浏览器...")
        driver = UtilsDriver.get_driver()
        driver.get("https://www.baidu.com")
        logger.info(f"页面标题: {driver.title}")
        UtilsDriver.quit_driver()
        logger.info("✓ Chrome浏览器正常工作")
        return 0
    except Exception as e:
        logger.error(f"✗ Chrome浏览器检查失败: {e}")
        return 1


def main():
    parser = argparse.ArgumentParser(description='自动化测试框架')
    parser.add_argument('--demo', action='store_true', help='演示模式，展示框架结构')
    parser.add_argument('--test', action='store_true', help='运行所有测试')
    parser.add_argument('--pytest', action='store_true', help='运行pytest参数化测试')
    parser.add_argument('--ddt', action='store_true', help='运行DDT测试')
    parser.add_argument('--check-chrome', action='store_true', help='检查Chrome浏览器')
    parser.add_argument('--file', help='指定测试文件运行')
    parser.add_argument('--debug', action='store_true', help='调试模式，显示详细日志')
    
    # 如果是通过python -m pytest调用，直接执行
    if len(sys.argv) > 1 and sys.argv[1] == '-m' and sys.argv[2] == 'pytest':
        pytest.main(sys.argv[3:])
        return
    
    args = parser.parse_args()
    
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    
    if args.demo:
        demo_mode()
    elif args.test:
        sys.exit(run_tests())
    elif args.pytest:
        sys.exit(run_pytest_tests())
    elif args.ddt:
        sys.exit(run_ddt_tests())
    elif args.check_chrome:
        sys.exit(check_chrome())
    elif args.file:
        sys.exit(run_tests(args.file))
    else:
        # 没有参数时显示帮助
        print("=" * 60)
        print("自动化测试框架 - Docker 版本")
        print("=" * 60)
        print("\n使用方法:")
        print("  python main.py --demo        演示模式")
        print("  python main.py --test        运行所有测试")
        print("  python main.py --pytest      运行pytest参数化测试")
        print("  python main.py --ddt         运行DDT测试")
        print("  python main.py --check-chrome 检查Chrome浏览器")
        print("  python main.py --file tests/test_login.py 运行指定测试文件")
        print("\nDocker使用示例:")
        print("  docker run --rm test-framework --demo")
        print("  docker run --rm --network host test-framework --test")
        print("")
        demo_mode()


if __name__ == '__main__':
    main()
