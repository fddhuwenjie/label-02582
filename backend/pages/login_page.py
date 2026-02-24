"""
LoginPage - 登录页面对象
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage, BaseHandle
import logging

logger = logging.getLogger(__name__)


class LoginPageLocator:
    """登录页面元素定位器"""
    USERNAME_INPUT = (By.NAME, "username")
    PASSWORD_INPUT = (By.NAME, "password")
    VERIFY_CODE_INPUT = (By.NAME, "verify_code")
    LOGIN_BTN = (By.XPATH, "//a[@name='sbtbutton']")
    ERROR_MSG = (By.CLASS_NAME, "error-msg")
    SUCCESS_MSG = (By.CLASS_NAME, "username")


class LoginPage(BasePage):
    """登录页面类"""
    
    def __init__(self, driver):
        super().__init__(driver)
        self.locator = LoginPageLocator()
    
    def get_username_input(self):
        """获取用户名输入框"""
        return self.find_element_by_name(self.locator.USERNAME_INPUT[1])
    
    def get_password_input(self):
        """获取密码输入框"""
        return self.find_element_by_name(self.locator.PASSWORD_INPUT[1])
    
    def get_verify_code_input(self):
        """获取验证码输入框"""
        return self.find_element_by_name(self.locator.VERIFY_CODE_INPUT[1])
    
    def get_login_btn(self):
        """获取登录按钮"""
        return self.find_element_by_xpath(self.locator.LOGIN_BTN[1])
    
    def get_error_msg(self):
        """获取错误提示"""
        try:
            return self.find_element_by_class(self.locator.ERROR_MSG[1])
        except:
            return None
    
    def get_success_element(self):
        """获取登录成功后的用户名元素"""
        try:
            return self.find_element_by_class(self.locator.SUCCESS_MSG[1])
        except:
            return None


class LoginPageHandle(BaseHandle):
    """登录页面操作处理类"""
    
    def __init__(self, driver):
        super().__init__(driver)
        self.page = LoginPage(driver)
    
    def input_username(self, username):
        """输入用户名"""
        logger.info(f"输入用户名: {username}")
        element = self.page.get_username_input()
        self.input_text(element, username)
    
    def input_password(self, password):
        """输入密码"""
        logger.info("输入密码: ******")
        element = self.page.get_password_input()
        self.input_text(element, password)
    
    def input_verify_code(self, code):
        """输入验证码"""
        logger.info(f"输入验证码: {code}")
        element = self.page.get_verify_code_input()
        self.input_text(element, code)
    
    def click_login(self):
        """点击登录按钮"""
        logger.info("点击登录按钮")
        element = self.page.get_login_btn()
        self.click_element(element)
    
    def login(self, username, password, verify_code="8888"):
        """执行登录操作"""
        logger.info(f"执行登录: {username}")
        self.input_username(username)
        self.input_password(password)
        self.input_verify_code(verify_code)
        self.click_login()
    
    def get_login_result(self):
        """获取登录结果"""
        # 检查是否有错误提示
        error = self.page.get_error_msg()
        if error and self.is_element_displayed(error):
            return {"success": False, "message": self.get_element_text(error)}
        
        # 检查是否登录成功
        success = self.page.get_success_element()
        if success and self.is_element_displayed(success):
            return {"success": True, "message": "登录成功"}
        
        return {"success": False, "message": "未知状态"}
