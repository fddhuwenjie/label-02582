"""
conftest.py - pytest 配置文件
"""
import pytest
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# 仅在selenium可用时导入driver相关fixture
try:
    from utils.driver import UtilsDriver
    
    @pytest.fixture(scope="session")
    def driver():
        """浏览器驱动 fixture"""
        drv = UtilsDriver.get_driver()
        yield drv
        UtilsDriver.quit_driver()

    @pytest.fixture(scope="function")
    def navigate_to_home(driver):
        """导航到首页"""
        from config import BASE_URL
        UtilsDriver.navigate_to(BASE_URL)
        return driver
        
except ImportError:
    # selenium未安装时跳过driver相关fixture
    pass
