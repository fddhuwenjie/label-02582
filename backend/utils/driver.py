"""
UtilsDriver - 浏览器驱动工具类
单例模式管理WebDriver实例
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from config import HEADLESS, IMPLICIT_WAIT, PAGE_LOAD_TIMEOUT
import logging
import os

logger = logging.getLogger(__name__)

# 远程Selenium配置
SELENIUM_REMOTE_URL = os.getenv("SELENIUM_REMOTE_URL")
DOCKER_ENV = os.getenv("DOCKER_ENV", "false").lower() == "true"
CHROME_BIN = os.getenv("CHROME_BIN")


class UtilsDriver:
    """
    浏览器驱动工具类
    使用单例模式确保整个测试过程只有一个浏览器实例
    """
    
    _driver = None
    
    @classmethod
    def get_driver(cls):
        """
        获取浏览器驱动实例（单例模式）
        :return: WebDriver实例
        """
        if cls._driver is None:
            cls._driver = cls._init_driver()
        return cls._driver
    
    @classmethod
    def _init_driver(cls):
        """
        初始化浏览器驱动
        :return: WebDriver实例
        """
        logger.info("初始化 Chrome 浏览器驱动...")
        
        options = Options()
        options.add_argument('--start-maximized')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-infobars')
        options.add_argument('--remote-debugging-port=9222')
        
        # 设置Chrome二进制路径（如果指定）
        if CHROME_BIN:
            options.binary_location = CHROME_BIN
            logger.info(f"使用Chrome二进制路径: {CHROME_BIN}")
        
        # Docker环境特殊配置
        if DOCKER_ENV:
            options.add_argument('--headless=new')
            options.add_argument('--disable-software-rasterizer')
            logger.info("Docker环境: 启用特殊浏览器配置")
        elif HEADLESS:
            options.add_argument('--headless=new')
            logger.info("使用无头模式运行")
        
        try:
            # 检查是否使用远程Selenium
            if SELENIUM_REMOTE_URL:
                logger.info(f"使用远程Selenium驱动: {SELENIUM_REMOTE_URL}")
                driver = webdriver.Remote(
                    command_executor=SELENIUM_REMOTE_URL,
                    options=options
                )
            else:
                # 本地Chrome驱动
                if DOCKER_ENV:
                    # Docker内使用系统安装的ChromeDriver
                    chrome_driver_path = os.getenv("CHROME_DRIVER_PATH", "/usr/bin/chromedriver")
                    logger.info(f"使用系统ChromeDriver: {chrome_driver_path}")
                    service = Service(chrome_driver_path)
                else:
                    service = Service(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service, options=options)
            
            # 设置隐式等待
            driver.implicitly_wait(IMPLICIT_WAIT)
            # 设置页面加载超时
            driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
            
            logger.info("浏览器驱动初始化成功")
            return driver
        except Exception as e:
            logger.error(f"浏览器驱动初始化失败: {e}")
            raise
    
    @classmethod
    def set_window_size(cls, width, height):
        """
        设置窗口大小
        :param width: 宽度
        :param height: 高度
        """
        driver = cls.get_driver()
        driver.set_window_size(width, height)
        logger.info(f"窗口大小设置为: {width}x{height}")
    
    @classmethod
    def maximize_window(cls):
        """最大化窗口"""
        driver = cls.get_driver()
        driver.maximize_window()
        logger.info("窗口已最大化")
    
    @classmethod
    def navigate_to(cls, url):
        """
        导航到指定 URL
        :param url: 目标URL
        """
        driver = cls.get_driver()
        try:
            driver.get(url)
            logger.info(f"导航到: {url}")
        except Exception as e:
            logger.error(f"导航失败: {url}, 错误: {e}")
            raise
    
    @classmethod
    def quit_driver(cls):
        """关闭浏览器并清理资源"""
        if cls._driver:
            try:
                cls._driver.quit()
                logger.info("浏览器已关闭")
            except Exception as e:
                logger.warning(f"关闭浏览器时出错: {e}")
            finally:
                cls._driver = None
    
    @classmethod
    def refresh(cls):
        """刷新页面"""
        driver = cls.get_driver()
        driver.refresh()
        logger.info("页面已刷新")
    
    @classmethod
    def back(cls):
        """浏览器后退"""
        driver = cls.get_driver()
        driver.back()
        logger.info("浏览器后退")
    
    @classmethod
    def forward(cls):
        """浏览器前进"""
        driver = cls.get_driver()
        driver.forward()
        logger.info("浏览器前进")
    
    @classmethod
    def get_current_url(cls):
        """
        获取当前 URL
        :return: 当前页面URL
        """
        return cls.get_driver().current_url
    
    @classmethod
    def get_title(cls):
        """
        获取页面标题
        :return: 页面标题
        """
        return cls.get_driver().title
    
    @classmethod
    def get_page_source(cls):
        """
        获取页面源码
        :return: 页面HTML源码
        """
        return cls.get_driver().page_source
    
    @classmethod
    def delete_all_cookies(cls):
        """删除所有Cookie"""
        cls.get_driver().delete_all_cookies()
        logger.info("已删除所有Cookie")
    
    @classmethod
    def add_cookie(cls, cookie_dict):
        """
        添加Cookie
        :param cookie_dict: Cookie字典
        """
        cls.get_driver().add_cookie(cookie_dict)
        logger.info(f"已添加Cookie: {cookie_dict.get('name')}")
    
    @classmethod
    def get_cookies(cls):
        """
        获取所有Cookie
        :return: Cookie列表
        """
        return cls.get_driver().get_cookies()
