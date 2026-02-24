"""
BasePage - 页面基类
BaseHandle - 页面操作处理基类
"""
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    TimeoutException, 
    NoSuchElementException, 
    ElementNotInteractableException,
    StaleElementReferenceException
)
import logging
import time
import os
from config import SCREENSHOT_DIR, EXPLICIT_WAIT

logger = logging.getLogger(__name__)


class BasePage:
    """
    页面元素定位基类
    封装各种定位方法，提供统一的元素查找接口
    """
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, EXPLICIT_WAIT)
    
    def find_element_by_id(self, element_id):
        """通过 ID 定位元素"""
        try:
            return self.wait.until(EC.presence_of_element_located((By.ID, element_id)))
        except TimeoutException:
            logger.error(f"元素定位超时: ID={element_id}")
            raise
    
    def find_element_by_class(self, class_name):
        """通过 Class 定位元素"""
        try:
            return self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, class_name)))
        except TimeoutException:
            logger.error(f"元素定位超时: CLASS={class_name}")
            raise
    
    def find_element_by_xpath(self, xpath):
        """通过 XPath 定位元素"""
        try:
            return self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        except TimeoutException:
            logger.error(f"元素定位超时: XPATH={xpath}")
            raise
    
    def find_element_by_css(self, css_selector):
        """通过 CSS 选择器定位元素"""
        try:
            return self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
        except TimeoutException:
            logger.error(f"元素定位超时: CSS={css_selector}")
            raise
    
    def find_element_by_name(self, name):
        """通过 Name 定位元素"""
        try:
            return self.wait.until(EC.presence_of_element_located((By.NAME, name)))
        except TimeoutException:
            logger.error(f"元素定位超时: NAME={name}")
            raise
    
    def find_element_by_link_text(self, link_text):
        """通过链接文本定位元素"""
        try:
            return self.wait.until(EC.presence_of_element_located((By.LINK_TEXT, link_text)))
        except TimeoutException:
            logger.error(f"元素定位超时: LINK_TEXT={link_text}")
            raise
    
    def find_element_by_partial_link_text(self, partial_text):
        """通过部分链接文本定位元素"""
        try:
            return self.wait.until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, partial_text)))
        except TimeoutException:
            logger.error(f"元素定位超时: PARTIAL_LINK_TEXT={partial_text}")
            raise
    
    def find_elements_by_xpath(self, xpath):
        """通过 XPath 定位多个元素"""
        return self.driver.find_elements(By.XPATH, xpath)
    
    def find_elements_by_css(self, css_selector):
        """通过 CSS 选择器定位多个元素"""
        return self.driver.find_elements(By.CSS_SELECTOR, css_selector)
    
    def find_elements_by_class(self, class_name):
        """通过 Class 定位多个元素"""
        return self.driver.find_elements(By.CLASS_NAME, class_name)
    
    def is_element_present(self, by, value, timeout=3):
        """检查元素是否存在"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return True
        except TimeoutException:
            return False


class BaseHandle:
    """
    页面操作处理基类
    封装输入、点击、等待等公共操作方法
    """
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, EXPLICIT_WAIT)
    
    def wait_element_visible(self, locator, timeout=None):
        """等待元素可见"""
        wait = WebDriverWait(self.driver, timeout or EXPLICIT_WAIT)
        try:
            return wait.until(EC.visibility_of_element_located(locator))
        except TimeoutException:
            logger.error(f"等待元素可见超时: {locator}")
            raise
    
    def wait_element_clickable(self, locator, timeout=None):
        """等待元素可点击"""
        wait = WebDriverWait(self.driver, timeout or EXPLICIT_WAIT)
        try:
            return wait.until(EC.element_to_be_clickable(locator))
        except TimeoutException:
            logger.error(f"等待元素可点击超时: {locator}")
            raise
    
    def wait_element_invisible(self, locator, timeout=None):
        """等待元素不可见"""
        wait = WebDriverWait(self.driver, timeout or EXPLICIT_WAIT)
        try:
            return wait.until(EC.invisibility_of_element_located(locator))
        except TimeoutException:
            logger.error(f"等待元素不可见超时: {locator}")
            raise
    
    def wait_text_present(self, locator, text, timeout=None):
        """等待元素包含指定文本"""
        wait = WebDriverWait(self.driver, timeout or EXPLICIT_WAIT)
        try:
            return wait.until(EC.text_to_be_present_in_element(locator, text))
        except TimeoutException:
            logger.error(f"等待文本出现超时: {locator}, text={text}")
            raise
    
    def input_text(self, element, text, clear_first=True):
        """
        输入文本
        :param element: 目标元素
        :param text: 要输入的文本
        :param clear_first: 是否先清空
        """
        try:
            if clear_first:
                element.clear()
            element.send_keys(text)
            logger.info(f"输入文本: {text[:20]}..." if len(str(text)) > 20 else f"输入文本: {text}")
        except ElementNotInteractableException:
            logger.error("元素不可交互，无法输入文本")
            raise
    
    def click_element(self, element, retry=3):
        """
        点击元素（带重试机制）
        :param element: 目标元素
        :param retry: 重试次数
        """
        for i in range(retry):
            try:
                element.click()
                logger.info("点击元素成功")
                return
            except (ElementNotInteractableException, StaleElementReferenceException) as e:
                if i < retry - 1:
                    logger.warning(f"点击失败，重试 {i+1}/{retry}: {e}")
                    time.sleep(0.5)
                else:
                    logger.error(f"点击元素失败: {e}")
                    raise
    
    def get_element_text(self, element):
        """获取元素文本"""
        try:
            return element.text
        except StaleElementReferenceException:
            logger.error("元素已过期，无法获取文本")
            raise
    
    def get_element_attribute(self, element, attribute):
        """获取元素属性"""
        try:
            return element.get_attribute(attribute)
        except StaleElementReferenceException:
            logger.error(f"元素已过期，无法获取属性: {attribute}")
            raise
    
    def is_element_displayed(self, element):
        """判断元素是否显示"""
        try:
            return element.is_displayed()
        except (NoSuchElementException, StaleElementReferenceException):
            return False
    
    def is_element_enabled(self, element):
        """判断元素是否可用"""
        try:
            return element.is_enabled()
        except (NoSuchElementException, StaleElementReferenceException):
            return False
    
    def is_element_selected(self, element):
        """判断元素是否被选中"""
        try:
            return element.is_selected()
        except (NoSuchElementException, StaleElementReferenceException):
            return False
    
    def switch_to_alert(self, timeout=None):
        """切换到弹窗"""
        wait = WebDriverWait(self.driver, timeout or EXPLICIT_WAIT)
        try:
            return wait.until(EC.alert_is_present())
        except TimeoutException:
            logger.error("等待弹窗超时")
            raise
    
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
    
    def get_alert_text(self):
        """获取弹窗文本"""
        alert = self.switch_to_alert()
        return alert.text
    
    def switch_to_frame(self, frame):
        """切换到iframe"""
        self.driver.switch_to.frame(frame)
        logger.info("切换到iframe")
    
    def switch_to_default_content(self):
        """切换回主文档"""
        self.driver.switch_to.default_content()
        logger.info("切换回主文档")
    
    def switch_to_window(self, window_handle):
        """切换到指定窗口"""
        self.driver.switch_to.window(window_handle)
        logger.info(f"切换到窗口: {window_handle}")
    
    def get_current_window_handle(self):
        """获取当前窗口句柄"""
        return self.driver.current_window_handle
    
    def get_all_window_handles(self):
        """获取所有窗口句柄"""
        return self.driver.window_handles
    
    def take_screenshot(self, name):
        """
        截图保存
        :param name: 截图名称
        :return: 截图文件路径
        """
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
    
    def scroll_to_element(self, element):
        """滚动到元素位置"""
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        logger.info("滚动到元素位置")
    
    def scroll_to_top(self):
        """滚动到页面顶部"""
        self.driver.execute_script("window.scrollTo(0, 0);")
        logger.info("滚动到页面顶部")
    
    def scroll_to_bottom(self):
        """滚动到页面底部"""
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        logger.info("滚动到页面底部")
    
    def execute_script(self, script, *args):
        """执行JavaScript脚本"""
        return self.driver.execute_script(script, *args)
