import os
import importlib
from typing import Callable
# from main_window_ui import MainWindowUI
from plugin_card import create_card


class MainWindowLogic:
    """处理主窗口的业务逻辑，与UI解耦"""

    def __init__(self):
        # self.ui = ui
        self.plugins = []
        self.load_test_plugins()

    def load_test_plugins(self):
        """测试插件"""
        from plugins.test_plugin.index import TestPlugin

        # self.plugins.append(TestPlugin())
        self.plugins = [TestPlugin() for i in range(23)]

    def test(self):
        print('test_method')

    def get_page_card(self, page_num=1):
        """
        根据传入的页数返回当页的所有卡片对象, 将所有插件9个分为1组，第一页就是第一组，返回包含行列信息的列表,3x3
        :param page_num: int
        :return: list[[card_obj,0,0],[card_obj,0,1]]
        """
        if page_num < 1:
            raise ValueError("页码必须大于等于1")

        # 每页9个插件 (3x3网格)
        per_page = 9
        start_idx = (page_num - 1) * per_page
        end_idx = start_idx + per_page
        print(start_idx, end_idx)
        page_plugins = self.plugins[start_idx:end_idx]

        # 生成带网格位置信息的卡片列表
        cards_with_pos = []
        for idx, plugin in enumerate(page_plugins):
            row = idx // 3  # 行索引 (0-2)
            col = idx % 3  # 列索引 (0-2)

            # 创建卡片对象 (根据实际需求调整Card初始化)
            card = create_card(plugin)
            cards_with_pos.append((card, row, col))
        return cards_with_pos

    # def load_plugins(self):
    #     """动态加载所有插件，其实就是把所有的插件实例化，并添加到self.plugins"""
    #     plugin_dir = "../plugins"
    #     for plugin_name in os.listdir(plugin_dir):
    #         if not os.path.isdir(os.path.join(plugin_dir, plugin_name)):
    #             continue
    #
    #         try:
    #             module = importlib.import_module(f"plugins.{plugin_name}.ui")
    #             btn = self.ui.add_plugin_button(module.PLUGIN_NAME)
    #             btn.clicked.connect(self.make_plugin_opener(module))
    #             self.plugins[plugin_name] = module
    #         except ImportError as e:
    #             print(f"加载插件失败: {plugin_name}\nError: {e}")
    #
    # def make_plugin_opener(self, module) -> Callable:
    #     """生成插件打开函数的闭包"""
    #
    #     def open_plugin():
    #         plugin_window = module.PluginWindow()
    #         plugin_window.exec()
    #
    #     return open_plugin