from abc import ABC, abstractmethod
from PyQt6.QtGui import QIcon


class BasePlugin(ABC):
    # 插件基类，所有插件都应该继承此类
    @property
    @abstractmethod
    def name(self):
        """插件名称"""
        pass
    @abstractmethod
    def icon(self):
        """插件图标"""
        return QIcon("../icons/plugin_default_icon.svg")

    @property
    @abstractmethod
    def version(self) -> str:
        """插件版本号"""
        pass

    @abstractmethod
    def create_window(self):
        """创建窗口"""
        pass
