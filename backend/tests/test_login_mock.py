"""
登录功能测试用例 - Mock模式
无需真实TPshop环境，可直接运行验证框架功能
"""
import unittest
import json
import os
import time
import logging
from ddt import ddt, data

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


class MockLoginPage:
    """模拟登录页面 - 用于演示PO模式"""
    
    # 模拟的有效账号
    VALID_USERS = {
        "13800138000": "123456"
    }
    VALID_VERIFY_CODE = "8888"
    
    def __init__(self):
        self.current_username = None
        self.current_password = None
        self.current_verify_code = None
        self.error_message = None
        self.is_logged_in = False
    
    def input_username(self, username):
        """输入用户名"""
        logger.info(f"输入用户名: {username}")
        self.current_username = username
        time.sleep(0.1)  # 模拟操作延迟
    
    def input_password(self, password):
        """输入密码"""
        logger.info(f"输入密码: {'*' * len(password) if password else '(空)'}")
        self.current_password = password
        time.sleep(0.1)
    
    def input_verify_code(self, code):
        """输入验证码"""
        logger.info(f"输入验证码: {code if code else '(空)'}")
        self.current_verify_code = code
        time.sleep(0.1)
    
    def click_login(self):
        """点击登录按钮"""
        logger.info("点击登录按钮")
        time.sleep(0.2)  # 模拟点击延迟
        self._validate_login()
    
    def _validate_login(self):
        """验证登录逻辑"""
        # 检查用户名
        if not self.current_username:
            self.error_message = "请输入用户名"
            self.is_logged_in = False
            return
        
        # 检查密码
        if not self.current_password:
            self.error_message = "请输入密码"
            self.is_logged_in = False
            return
        
        # 检查验证码
        if not self.current_verify_code:
            self.error_message = "请输入验证码"
            self.is_logged_in = False
            return
        
        if self.current_verify_code != self.VALID_VERIFY_CODE:
            self.error_message = "验证码错误"
            self.is_logged_in = False
            return
        
        # 检查用户名密码
        if self.current_username not in self.VALID_USERS:
            self.error_message = "用户名不存在"
            self.is_logged_in = False
            return
        
        if self.VALID_USERS[self.current_username] != self.current_password:
            self.error_message = "密码错误"
            self.is_logged_in = False
            return
        
        # 登录成功
        self.error_message = None
        self.is_logged_in = True
    
    def get_login_result(self):
        """获取登录结果"""
        if self.is_logged_in:
            return {"success": True, "message": "登录成功"}
        else:
            return {"success": False, "message": self.error_message}
    
    def reset(self):
        """重置状态"""
        self.current_username = None
        self.current_password = None
        self.current_verify_code = None
        self.error_message = None
        self.is_logged_in = False


@ddt
class TestLoginMock(unittest.TestCase):
    """
    登录功能测试类 - Mock模式
    使用DDT数据驱动，演示完整的测试流程
    """
    
    @classmethod
    def setUpClass(cls):
        """测试类初始化"""
        logger.info("=" * 60)
        logger.info("TPshop商城登录功能自动化测试")
        logger.info("测试模式: Mock模拟测试")
        logger.info("=" * 60)
        cls.login_page = MockLoginPage()
        cls.test_results = []
        cls.start_time = time.time()
    
    @classmethod
    def tearDownClass(cls):
        """测试类清理"""
        elapsed = time.time() - cls.start_time
        logger.info("=" * 60)
        logger.info("测试执行完成")
        logger.info(f"总用例数: {len(cls.test_results)}")
        passed = sum(1 for r in cls.test_results if r['passed'])
        failed = len(cls.test_results) - passed
        logger.info(f"通过: {passed}, 失败: {failed}")
        logger.info(f"通过率: {passed/len(cls.test_results)*100:.1f}%")
        logger.info(f"执行时间: {elapsed:.2f}s")
        logger.info("=" * 60)
        
        # 打印详细结果
        logger.info("\n测试结果详情:")
        for result in cls.test_results:
            status = "✓ PASSED" if result['passed'] else "✗ FAILED"
            logger.info(f"  {result['case_id']}: {result['description']} - {status}")
    
    def setUp(self):
        """每个测试方法前执行"""
        self.login_page.reset()
    
    @data(*load_test_data())
    def test_login(self, test_data):
        """
        登录功能测试
        使用DDT库的@data装饰器实现数据驱动
        从JSON文件读取测试数据
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
        logger.info(f"预期结果: {expected}")
        
        test_passed = False
        
        try:
            # 执行登录操作
            self.login_page.input_username(username)
            self.login_page.input_password(password)
            self.login_page.input_verify_code(verify_code)
            self.login_page.click_login()
            
            # 获取结果
            result = self.login_page.get_login_result()
            logger.info(f"实际结果: {'成功' if result['success'] else '失败'} - {result['message']}")
            
            # 断言
            if expected == "success":
                self.assertTrue(result['success'], f"期望登录成功，实际: {result['message']}")
                test_passed = True
            else:
                self.assertFalse(result['success'], f"期望登录失败，实际登录成功")
                test_passed = True
            
            logger.info(f"✓ 测试通过: {case_id}")
            
        except AssertionError as e:
            logger.error(f"✗ 测试失败: {case_id} - {e}")
            raise
        finally:
            self.__class__.test_results.append({
                'case_id': case_id,
                'description': description,
                'passed': test_passed
            })


if __name__ == '__main__':
    # 运行测试
    unittest.main(verbosity=2)
