"""
工具模块初始化
"""
# 仅在selenium可用时导入
try:
    from utils.driver import UtilsDriver
    __all__ = ['UtilsDriver']
except ImportError:
    __all__ = []
