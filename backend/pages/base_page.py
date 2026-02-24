"""
BasePage - 页面基类
"""
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import logging

logger = logging.getLogger(__name__)


class BasePage:
    """页面元素定位基类"""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def find_element_by_id(self, element_id):
        """通过 ID 定位元素"""
        return self.wait.until(EC.presence_of_element_located((By.ID, element_id)))
    
    def find_element_by_class(self, class_name):
        """通过 Class 定位元素"""
        return self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, class_name)))
    
    def find_element_by_xpath(self, xpath):
        """通过 XPath 定位元素"""
        return self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
    
    def find_element_by_css(self, css_selector):
        """通过 CSS 选择器定位元素"""
        return self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
    
    def find_element_by_name(self, name):
        """通过 Name 定位元素"""
        return self.wait.until(EC.presence_of_element_located((By.NAME, name)))
    
    def find_element_by_link_text(self, link_text):
        """通过链接文本定位元素"""
        return self.wait.until(EC.presence_of_element_located((By.LINK_TEXT, link_text)))
    
    def find_elements_by_xpath(self, xpath):
        """通过 XPath 定位多个元素"""
        return self.driver.find_elements(By.XPATH, xpath)
    
    def find_elements_by_css(self, css_selector):
        """通过 CSS 选择器定位多个元素"""
        return self.driver.find_elements(By.CSS_SELECTOR, css_selector)


class BaseHandle:
    """页面操作处理基类"""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def wait_element_visible(self, locator):
        """等待元素可见"""
        return self.wait.until(EC.visibility_of_element_located(locator))
    
    def wait_element_clickable(self, locator):
        """等待元素可点击"""
        return self.wait.until(EC.element_to_be_clickable(locator))
    
    def input_text(self, element, text):
        """输入文本"""
        element.clear()
        element.send_keys(text)
        logger.info(f"输入文本: {text}")
    
    def click_element(self, element):
        """点击元素"""
        element.click()
        logger.info("点击元素")
    
    def get_element_text(self, element):
        """获取元素文本"""
        return element.text
    
    def get_element_attribute(self, element, attribute):
        """获取元素属性"""
        return element.get_attribute(attribute)
    
    def is_element_displayed(self, element):
        """判断元素是否显示"""
        try:
            return element.is_displayed()
        except:
            return False
    
    def switch_to_alert(self):
        """切换到弹窗"""
        return self.wait.until(EC.alert_is_present())
    
    def accept_alert(self):
        """确认弹窗"""
        alert = self.switch_to_alert()
        alert.accept()
        logger.info("确认弹窗")
    
    def dismiss_alert(self):
        """取消弹窗"""
        alert = self.switch_to_alert()
        alert.dismiss()
        logger.info("取消弹窗")
