"""
登录功能测试用例 - 使用DDT库实现数据驱动
符合实验要求：使用DDT库从JSON文件读取测试数据
"""
import unittest
import json
import os
import logging
import time
from ddt import ddt, data, unpack, file_data
from utils.driver import UtilsDriver
from pages.home_page import HomePageHandle
from pages.login_page import LoginPageHandle
from config import BASE_URL, SCREENSHOT_DIR

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_test_data():
    """加载测试数据"""
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'login_data.json')
    with open(data_path, 'r', encoding='utf-8') as f:
        return json.load(f)


@ddt
class TestLoginDDT(unittest.TestCase):
    """
    登录功能测试类 - 使用DDT数据驱动
    DDT (Data-Driven Tests) 库实现数据驱动测试
    """
    
    @classmethod
    def setUpClass(cls):
        """测试类初始化"""
        logger.info("=" * 60)
        logger.info("开始登录功能测试 (DDT数据驱动)")
        logger.info("=" * 60)
        cls.driver = UtilsDriver.get_driver()
        cls.home_handle = HomePageHandle(cls.driver)
        cls.login_handle = LoginPageHandle(cls.driver)
        cls.test_results = []
    
    @classmethod
    def tearDownClass(cls):
        """测试类清理"""
        logger.info("=" * 60)
        logger.info("登录功能测试结束")
        logger.info(f"测试结果汇总: {len(cls.test_results)} 个用例")
        for result in cls.test_results:
            status = "✓ 通过" if result['passed'] else "✗ 失败"
            logger.info(f"  {result['case_id']}: {status}")
        logger.info("=" * 60)
        UtilsDriver.quit_driver()
    
    def setUp(self):
        """每个测试方法前执行"""
        try:
            UtilsDriver.navigate_to(BASE_URL)
            time.sleep(1)
            self.home_handle.click_login()
            time.sleep(1)
        except Exception as e:
            logger.error(f"测试准备失败: {e}")
            self.take_screenshot("setup_error")
    
    def tearDown(self):
        """每个测试方法后执行"""
        pass
    
    def take_screenshot(self, name):
        """截图保存"""
        try:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"{name}_{timestamp}.png"
            filepath = os.path.join(SCREENSHOT_DIR, filename)
            self.driver.save_screenshot(filepath)
            logger.info(f"截图已保存: {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"截图失败: {e}")
            return None
    
    @data(*load_test_data())
    def test_login(self, test_data):
        """
        登录功能测试
        使用 DDT 库的 @data 装饰器实现数据驱动
        从 JSON 文件读取测试数据
        """
        case_id = test_data['case_id']
        description = test_data['description']
        username = test_data['username']
        password = test_data['password']
        verify_code = test_data.get('verify_code', '8888')
        expected = test_data['expected']
        
        logger.info(f"\n{'='*50}")
        logger.info(f"执行测试用例: {case_id}")
        logger.info(f"用例描述: {description}")
        logger.info(f"测试数据: username={username}, password={'*'*len(password) if password else '空'}")
        logger.info(f"预期结果: {expected}")
        
        test_passed = False
        error_msg = None
        
        try:
            # 执行登录前截图
            self.take_screenshot(f"{case_id}_before_login")
            
            # 执行登录
            self.login_handle.login(username, password, verify_code)
            time.sleep(2)
            
            # 执行登录后截图
            self.take_screenshot(f"{case_id}_after_login")
            
            # 获取结果
            result = self.login_handle.get_login_result()
            
            # 断言
            if expected == "success":
                self.assertTrue(result['success'], f"期望登录成功，实际: {result['message']}")
                test_passed = True
                logger.info(f"✓ 测试通过: {case_id} - 登录成功")
            else:
                self.assertFalse(result['success'], f"期望登录失败，实际登录成功")
                test_passed = True
                logger.info(f"✓ 测试通过: {case_id} - 登录失败(符合预期)")
                
        except AssertionError as e:
            error_msg = str(e)
            logger.error(f"✗ 测试失败: {case_id} - {error_msg}")
            self.take_screenshot(f"{case_id}_error")
            raise
        except Exception as e:
            error_msg = str(e)
            logger.error(f"✗ 测试异常: {case_id} - {error_msg}")
            self.take_screenshot(f"{case_id}_exception")
            raise
        finally:
            # 记录测试结果
            self.__class__.test_results.append({
                'case_id': case_id,
                'description': description,
                'passed': test_passed,
                'error': error_msg
            })


if __name__ == '__main__':
    # 使用unittest运行DDT测试
    unittest.main(verbosity=2)
