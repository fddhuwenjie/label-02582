"""
LoginPage - 登录页面对象
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage, BaseHandle
from config import UNIVERSAL_VERIFY_CODE
import logging
import time

logger = logging.getLogger(__name__)


class LoginPageLocator:
    """登录页面元素定位器"""
    USERNAME_INPUT = (By.NAME, "username")
    PASSWORD_INPUT = (By.NAME, "password")
    VERIFY_CODE_INPUT = (By.NAME, "verify_code")
    LOGIN_BTN = (By.XPATH, "//a[@name='sbtbutton']")
    ERROR_MSG = (By.CLASS_NAME, "error-msg")
    SUCCESS_MSG = (By.CLASS_NAME, "username")
    # 备用定位器
    LOGIN_BTN_ALT = (By.CSS_SELECTOR, "a.btn-login")
    VERIFY_CODE_IMG = (By.ID, "verify_code_img")


class LoginPage(BasePage):
    """登录页面类 - 继承BasePage，定义登录页面特有元素"""
    
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
        try:
            return self.find_element_by_xpath(self.locator.LOGIN_BTN[1])
        except Exception:
            # 尝试备用定位器
            return self.find_element_by_css(self.locator.LOGIN_BTN_ALT[1])
    
    def get_verify_code_img(self):
        """获取验证码图片"""
        try:
            return self.find_element_by_id(self.locator.VERIFY_CODE_IMG[1])
        except Exception:
            return None
    
    def get_error_msg(self):
        """获取错误提示"""
        try:
            return self.find_element_by_class(self.locator.ERROR_MSG[1])
        except Exception:
            return None
    
    def get_success_element(self):
        """获取登录成功后的用户名元素"""
        try:
            return self.find_element_by_class(self.locator.SUCCESS_MSG[1])
        except Exception:
            return None


class LoginPageHandle(BaseHandle):
    """
    登录页面操作处理类 - 继承BaseHandle
    封装登录页面的业务操作逻辑
    """
    
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
    
    def refresh_verify_code(self):
        """刷新验证码"""
        logger.info("刷新验证码")
        verify_img = self.page.get_verify_code_img()
        if verify_img:
            self.click_element(verify_img)
            time.sleep(0.5)
    
    def login(self, username, password, verify_code=None):
        """
        执行登录操作
        :param username: 用户名
        :param password: 密码
        :param verify_code: 验证码，默认使用配置中的万能验证码
        """
        # 使用传入的验证码或配置中的万能验证码
        code = verify_code if verify_code is not None else UNIVERSAL_VERIFY_CODE
        
        logger.info(f"执行登录: {username}")
        self.input_username(username)
        self.input_password(password)
        self.input_verify_code(code)
        self.click_login()
    
    def get_login_result(self):
        """
        获取登录结果
        :return: dict包含success和message
        """
        time.sleep(1)  # 等待页面响应
        
        # 检查是否有错误提示
        error = self.page.get_error_msg()
        if error and self.is_element_displayed(error):
            error_text = self.get_element_text(error)
            logger.info(f"登录失败: {error_text}")
            return {"success": False, "message": error_text}
        
        # 检查是否登录成功
        success = self.page.get_success_element()
        if success and self.is_element_displayed(success):
            logger.info("登录成功")
            return {"success": True, "message": "登录成功"}
        
        # 检查URL变化判断登录状态
        current_url = self.driver.current_url
        if "user" in current_url or "member" in current_url:
            logger.info("登录成功(URL判断)")
            return {"success": True, "message": "登录成功"}
        
        logger.warning("登录状态未知")
        return {"success": False, "message": "未知状态"}
    
    def logout(self):
        """退出登录"""
        logger.info("执行退出登录")
        # 实现退出登录逻辑
        pass
