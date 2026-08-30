import os
import importlib
from typing import Callable
# from main_window_ui import MainWindowUI
from core.plugin_card import PluginCard
from core import logger
from core.config import PLUGINS_DIR
from core.plugin import BasePlugin
logger = logger.get_logger(__name__)


class MainWindowLogic:
    """处理主窗口的业务逻辑，与UI解耦"""

    def __init__(self):
        self.plugins = []
        self._filtered = []
        self.load_plugins()
        self._filtered = self.plugins[:]

    def load_test_plugins(self):
        """测试插件，实际上应该是动态加载所有插件"""
        from plugins.test_plugin import TestPlugin

        # 模拟加载23个插件实例
        self.plugins = [TestPlugin() for i in range(23)]

    def load_plugins(self):
        """加载所有plugins中的合法插件"""
        for plugin_name in os.listdir(PLUGINS_DIR):
            if not os.path.isdir(os.path.join(PLUGINS_DIR, plugin_name)):
                # 不是文件夹
                continue
            init_file = os.path.join(PLUGINS_DIR, plugin_name, '__init__.py')
            if not os.path.exists(init_file):
                # 没有__init__.py文件
                continue
            module_name = f"plugins.{plugin_name}"
            try:
                module = importlib.import_module(module_name)
                # 检查是否有__plugin_class__属性
                if not hasattr(module, '__plugin_class__'):
                    logger.error(f'模块 {module_name} 没有 __plugin_class__ 属性')
                    continue
                # 检测是否是BasePlugin的子类
                if not issubclass(getattr(module, '__plugin_class__'), BasePlugin):
                    logger.error(f'模块 {module_name} 的 __plugin_class__ 属性不是 BasePlugin 的子类')
                    continue
                # 实例化插件类
                plugin_class = getattr(module, '__plugin_class__')
                self.plugins.append(plugin_class())
                logger.debug(f'导入模块 {module_name} 成功')

            except ImportError as e:
                logger.error(f'导入模块 {module_name} 失败: {e}')

    def get_page_card(self, page_num=1, plugins=None):
        """
        根据传入的页数返回当页的所有卡片对象, 将所有插件9个分为1组，第一页就是第一组，返回包含行列信息的列表,3x3
        :param page_num: int
        :param plugins: 可选，指定插件列表（用于搜索过滤）
        :return: list[[card_obj,0,0],[card_obj,0,1]]
        """
        if page_num < 1:
            raise ValueError("页码必须大于等于1")
        src = plugins if plugins is not None else self._filtered
        per_page = 9
        start_idx = (page_num - 1) * per_page
        end_idx = start_idx + per_page
        page_plugins = src[start_idx:end_idx]

        cards_with_pos = []
        for idx, plugin in enumerate(page_plugins):
            row = idx // 3
            col = idx % 3
            card = PluginCard(plugin)
            cards_with_pos.append((card, row, col))
        return cards_with_pos

    def search(self, query):
        """按名称过滤插件，返回过滤后的列表"""
        q = query.strip().lower()
        if not q:
            self._filtered = self.plugins[:]
        else:
            self._filtered = [p for p in self.plugins if q in p.name.lower()]
        return self._filtered

    def open_plugin_window(self, plugin):
        """创建插件窗口"""
        logger.debug(f'打开插件窗口: {plugin.name}')
        plugin.create_window()


