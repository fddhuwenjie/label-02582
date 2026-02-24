"""
UtilsDriver - 浏览器驱动工具类
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import logging

logger = logging.getLogger(__name__)


class UtilsDriver:
    """浏览器驱动工具类"""
    
    _driver = None
    
    @classmethod
    def get_driver(cls):
        """获取浏览器驱动实例（单例模式）"""
        if cls._driver is None:
            cls._driver = cls._init_driver()
        return cls._driver
    
    @classmethod
    def _init_driver(cls):
        """初始化浏览器驱动"""
        logger.info("初始化 Chrome 浏览器驱动...")
        
        options = Options()
        options.add_argument('--start-maximized')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        # options.add_argument('--headless')  # 无头模式，测试时可开启
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        logger.info("浏览器驱动初始化成功")
        return driver
    
    @classmethod
    def set_window_size(cls, width, height):
        """设置窗口大小"""
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
        """导航到指定 URL"""
        driver = cls.get_driver()
        driver.get(url)
        logger.info(f"导航到: {url}")
    
    @classmethod
    def quit_driver(cls):
        """关闭浏览器"""
        if cls._driver:
            cls._driver.quit()
            cls._driver = None
            logger.info("浏览器已关闭")
    
    @classmethod
    def refresh(cls):
        """刷新页面"""
        driver = cls.get_driver()
        driver.refresh()
        logger.info("页面已刷新")
    
    @classmethod
    def get_current_url(cls):
        """获取当前 URL"""
        return cls.get_driver().current_url
    
    @classmethod
    def get_title(cls):
        """获取页面标题"""
        return cls.get_driver().title
