"""
HomePage - 商城首页页面对象
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage, BaseHandle
import logging

logger = logging.getLogger(__name__)


class HomePageLocator:
    """首页元素定位器"""
    LOGIN_LINK = (By.XPATH, "//a[contains(text(),'登录')]")
    REGISTER_LINK = (By.XPATH, "//a[contains(text(),'注册')]")
    SEARCH_INPUT = (By.ID, "q")
    SEARCH_BTN = (By.XPATH, "//button[@type='submit']")
    CART_LINK = (By.CLASS_NAME, "cart")
    LOGO = (By.CLASS_NAME, "logo")
    # 备用定位器
    LOGIN_LINK_ALT = (By.CSS_SELECTOR, "a.login")
    USER_INFO = (By.CLASS_NAME, "user-info")


class HomePage(BasePage):
    """
    商城首页页面类
    继承BasePage，定义首页特有元素
    """
    
    def __init__(self, driver):
        super().__init__(driver)
        self.locator = HomePageLocator()
    
    def get_login_link(self):
        """获取登录链接"""
        try:
            return self.find_element_by_xpath(self.locator.LOGIN_LINK[1])
        except Exception:
            return self.find_element_by_css(self.locator.LOGIN_LINK_ALT[1])
    
    def get_register_link(self):
        """获取注册链接"""
        return self.find_element_by_xpath(self.locator.REGISTER_LINK[1])
    
    def get_search_input(self):
        """获取搜索输入框"""
        return self.find_element_by_id(self.locator.SEARCH_INPUT[1])
    
    def get_search_btn(self):
        """获取搜索按钮"""
        return self.find_element_by_xpath(self.locator.SEARCH_BTN[1])
    
    def get_logo(self):
        """获取Logo元素"""
        return self.find_element_by_class(self.locator.LOGO[1])
    
    def is_user_logged_in(self):
        """检查用户是否已登录"""
        return self.is_element_present(By.CLASS_NAME, self.locator.USER_INFO[1])


class HomePageHandle(BaseHandle):
    """
    首页操作处理类
    继承BaseHandle，封装首页业务操作
    """
    
    def __init__(self, driver):
        super().__init__(driver)
        self.page = HomePage(driver)
    
    def click_login(self):
        """点击登录链接"""
        logger.info("点击登录链接")
        element = self.page.get_login_link()
        self.click_element(element)
    
    def click_register(self):
        """点击注册链接"""
        logger.info("点击注册链接")
        element = self.page.get_register_link()
        self.click_element(element)
    
    def search_product(self, keyword):
        """
        搜索商品
        :param keyword: 搜索关键词
        """
        logger.info(f"搜索商品: {keyword}")
        search_input = self.page.get_search_input()
        self.input_text(search_input, keyword)
        search_btn = self.page.get_search_btn()
        self.click_element(search_btn)
    
    def click_logo(self):
        """点击Logo返回首页"""
        logger.info("点击Logo返回首页")
        element = self.page.get_logo()
        self.click_element(element)
    
    def is_logged_in(self):
        """
        检查是否已登录
        :return: bool
        """
        return self.page.is_user_logged_in()
