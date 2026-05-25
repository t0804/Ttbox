import os
from abc import ABCMeta, ABC, abstractmethod
from PySide6.QtGui import QIcon
from core.config import ICONS_DIR
from core.logger import get_logger
logger = get_logger(__name__)


class PluginMeta(ABCMeta):
    def __new__(mcls, name, bases, namespace, **kwargs):
        cls = super().__new__(mcls, name, bases, namespace, **kwargs)

        # 检查是否为BasePlugin的子类（排除BasePlugin自身）
        if any(base.__name__ == 'BasePlugin' for base in bases) and name != 'BasePlugin':
            # 检查property
            if not isinstance(getattr(cls, 'name', None), property):
                raise TypeError(f"{name} 必须将 'name' 实现为@property")
            if not isinstance(getattr(cls, 'version', None), property):
                raise TypeError(f"{name} 必须将 'version' 实现为@property")

        return cls


class BasePlugin(ABC, metaclass=PluginMeta):
    # 插件基类，所有插件都应该继承此类
    @property
    @abstractmethod
    def name(self):
        """插件名称"""
        pass

    def icon(self):
        """插件图标"""
        return QIcon(os.path.join(ICONS_DIR, "plugin_default_icon.svg"))

    @property
    @abstractmethod
    def version(self) -> str:
        """插件版本号"""
        pass

    def create_window(self):
        """创建插件窗口

        注意：必须将窗口对象绑定到 self 上（如 self._window = XxxWindow()），
        否则局部变量会在函数返回后被 Python GC 回收，导致窗口闪退。

        正确写法：
            self._window = MyWindow()
            self._window.show()

        错误写法：
            MyWindow().show()              # 无引用 → 窗口闪退
            w = MyWindow(); w.show()       # 局部变量 → 函数结束即回收
        """
        logger.debug(f'插件无窗口')
        pass
