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


class HomePage(BasePage):
    """商城首页页面类"""
    
    def __init__(self, driver):
        super().__init__(driver)
        self.locator = HomePageLocator()
    
    def get_login_link(self):
        """获取登录链接"""
        return self.find_element_by_xpath(self.locator.LOGIN_LINK[1])
    
    def get_register_link(self):
        """获取注册链接"""
        return self.find_element_by_xpath(self.locator.REGISTER_LINK[1])
    
    def get_search_input(self):
        """获取搜索输入框"""
        return self.find_element_by_id(self.locator.SEARCH_INPUT[1])
    
    def get_search_btn(self):
        """获取搜索按钮"""
        return self.find_element_by_xpath(self.locator.SEARCH_BTN[1])


class HomePageHandle(BaseHandle):
    """首页操作处理类"""
    
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
        """搜索商品"""
        logger.info(f"搜索商品: {keyword}")
        search_input = self.page.get_search_input()
        self.input_text(search_input, keyword)
        search_btn = self.page.get_search_btn()
        self.click_element(search_btn)
