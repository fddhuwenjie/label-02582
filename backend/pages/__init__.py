"""
页面模块初始化
"""
from pages.base_page import BasePage, BaseHandle
from pages.home_page import HomePage, HomePageHandle
from pages.login_page import LoginPage, LoginPageHandle

__all__ = [
    'BasePage', 'BaseHandle',
    'HomePage', 'HomePageHandle', 
    'LoginPage', 'LoginPageHandle'
]
