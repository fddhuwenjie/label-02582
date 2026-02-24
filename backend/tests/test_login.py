"""
登录功能测试用例
使用 pytest + DDT 数据驱动
"""
import pytest
import json
import os
import logging
from utils.driver import UtilsDriver
from pages.home_page import HomePageHandle
from pages.login_page import LoginPageHandle

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 测试网站地址
BASE_URL = "http://localhost:8080"  # TPshop 本地部署地址


def load_test_data():
    """加载测试数据"""
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'login_data.json')
    with open(data_path, 'r', encoding='utf-8') as f:
        return json.load(f)


class TestLogin:
    """登录功能测试类"""
    
    @classmethod
    def setup_class(cls):
        """测试类初始化"""
        logger.info("=" * 50)
        logger.info("开始登录功能测试")
        logger.info("=" * 50)
        cls.driver = UtilsDriver.get_driver()
        cls.home_handle = HomePageHandle(cls.driver)
        cls.login_handle = LoginPageHandle(cls.driver)
    
    @classmethod
    def teardown_class(cls):
        """测试类清理"""
        logger.info("=" * 50)
        logger.info("登录功能测试结束")
        logger.info("=" * 50)
        UtilsDriver.quit_driver()
    
    def setup_method(self):
        """每个测试方法前执行"""
        UtilsDriver.navigate_to(BASE_URL)
        self.home_handle.click_login()
    
    @pytest.mark.parametrize("test_data", load_test_data(), ids=lambda x: x['case_id'])
    def test_login(self, test_data):
        """
        登录功能测试
        使用 DDT 数据驱动，从 JSON 文件读取测试数据
        """
        case_id = test_data['case_id']
        description = test_data['description']
        username = test_data['username']
        password = test_data['password']
        verify_code = test_data['verify_code']
        expected = test_data['expected']
        
        logger.info(f"执行测试用例: {case_id} - {description}")
        
        # 执行登录
        self.login_handle.login(username, password, verify_code)
        
        # 获取结果
        result = self.login_handle.get_login_result()
        
        # 断言
        if expected == "success":
            assert result['success'] == True, f"期望登录成功，实际: {result['message']}"
            logger.info(f"✓ 测试通过: {case_id}")
        else:
            assert result['success'] == False, f"期望登录失败，实际登录成功"
            logger.info(f"✓ 测试通过: {case_id}")


if __name__ == '__main__':
    pytest.main(['-v', '-s', __file__, '--html=reports/login_report.html'])
