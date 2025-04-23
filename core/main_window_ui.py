import datetime

from PyQt6.QtCore import Qt, QSize, QTimer, QDateTime
from PyQt6.QtGui import QIcon, QAction, QPixmap

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QGridLayout, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton,
    QFrame, QStatusBar, QStackedWidget
)

from pagination_controls import create_pagination_controls
from main_window_logic import MainWindowLogic


class MainWindowUI(QMainWindow):
    """仅负责主窗口界面布局，不包含业务逻辑"""

    def __init__(self):
        super().__init__()
        self._logic = MainWindowLogic()
        self.setWindowTitle("Ttbox")
        self.resize(1000, 700)

        # 菜单栏
        self.setup_menubar()
        # 中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        # 初始化状态栏和时间显示
        self.setup_statusbar()

        # 主布局（水平分割：左侧导航 + 右侧内容）
        self.main_layout = QHBoxLayout(central_widget)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(15)

        # 导航菜单
        self.navigation_content()

        # 右侧内容
        # ---- 右侧内容 ----
        self.stacked_widget = QStackedWidget()
        self.main_layout.addWidget(self.stacked_widget, stretch=1)
        self.init_pages()

    def init_pages(self):
        self.stacked_widget.addWidget(self.create_home_page())  # 首页
        self.stacked_widget.addWidget(self.create_other_page())  # 其他页
        self.stacked_widget.addWidget(self.create_settings_page())  # 设置页
        self.stacked_widget.setCurrentIndex(0)

    def create_home_page(self):
        # ---- 右侧内容 ----
        page = QWidget()
        # 垂直布局
        content_layout = QVBoxLayout(page)

        r_top = QFrame()
        r_top.setFixedHeight(40)
        # 顶部标题栏
        title_bar = QHBoxLayout(r_top)
        # title_bar = QHBoxLayout()
        title = QLabel("我的工具箱")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        search_box = QLineEdit()
        search_box.setPlaceholderText("搜索工具...")
        search_box.setFixedWidth(250)

        title_bar.addWidget(title)
        title_bar.addStretch()
        title_bar.addWidget(search_box)

        content_layout.addWidget(r_top)

        # 增加插件工具
        content_layout.addWidget(self.plugins_widget())

        return page

    def navigation_content(self):
        # ---- 左侧导航 ----
        nav_frame = QFrame()
        nav_frame.setFixedWidth(200)
        nav_frame.setStyleSheet("background-color: #f5f5f5;")
        nav_layout = QVBoxLayout(nav_frame)
        nav_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        # 导航项
        btn1 = QPushButton(QIcon("icons/folder.svg"), '全部工具')
        btn1.setFixedHeight(80)

        # 单击按钮后执行的函数，逻辑较简单没有必要放到logic类
        def btn1_click():
            print('点击了按钮btn1')
            self.stacked_widget.setCurrentIndex(0)

        btn1.clicked.connect(btn1_click)

        btn2 = QPushButton(QIcon("icons/folder.svg"), '其他')
        btn2.setFixedHeight(80)

        # 单击按钮后执行的函数

        def btn2_click():
            print('点击了按钮btn2')
            self.stacked_widget.setCurrentIndex(1)

        btn2.clicked.connect(btn2_click)

        btn3 = QPushButton(QIcon("icons/folder.svg"), '设置')
        btn3.setFixedHeight(80)

        # 第一个按钮

        # 单击按钮后执行的函数
        def btn3_click():
            print('点击了按钮btn3')
            self.stacked_widget.setCurrentIndex(2)

        btn3.clicked.connect(btn3_click)

        nav_layout.addWidget(btn1)
        nav_layout.addWidget(btn2)
        nav_layout.addWidget(btn3)
        self.main_layout.addWidget(nav_frame)

    def setup_menubar(self):
        """设置菜单栏"""
        menubar = self.menuBar()

        # 文件菜单
        file_menu = menubar.addMenu("文件")

        new_action = QAction("新建", self)
        open_action = QAction("打开", self)
        exit_action = QAction("退出", self)
        exit_action.triggered.connect(self.close)

        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)

        # 编辑菜单
        edit_menu = menubar.addMenu("编辑")
        cut_action = QAction("剪切", self)
        copy_action = QAction("复制", self)
        edit_menu.addActions([cut_action, copy_action])

        # 帮助菜单
        help_menu = menubar.addMenu("帮助")
        about_action = QAction("关于", self)
        help_menu.addAction(about_action)

    def setup_statusbar(self):
        """设置状态栏（带实时时间）"""
        status_bar = QStatusBar()
        self.setStatusBar(status_bar)

        # 左侧固定信息
        status_bar.showMessage("就绪")

        # 右侧实时时间
        self.time_label = QLabel()
        status_bar.addPermanentWidget(self.time_label)

        # 定时更新时间
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # 每秒更新一次
        self.update_time()  # 立即显示

    def update_time(self):
        """更新时间显示"""
        current_time = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
        self.time_label.setText(f"🕒 {current_time}")

    def create_other_page(self):
        # 其他页
        page = QWidget()
        content_layout = QVBoxLayout(page)
        label1 = QLabel("此页是其他页")
        content_layout.addWidget(label1)

        return page

    def create_settings_page(self):
        # 设置页
        page = QWidget()
        content_layout = QVBoxLayout(page)
        label1 = QLabel("此页是设置页")
        content_layout.addWidget(label1)

        return page

    def plugins_widget(self):
        top_frame = QFrame()
        top_layout = QVBoxLayout(top_frame)
        # 添加插件部分
        # 插件展示区（使用QStackedWidget实现分页）
        plugin_stack = QStackedWidget()
        top_layout.addWidget(plugin_stack)
        # print(self._logic.plugins)
        # 在容器中添加卡片页
        if len(self._logic.plugins) % 9 == 0:
            max_page = len(self._logic.plugins) // 9
        else:
            max_page = len(self._logic.plugins) // 9 + 1
        for i in range(max_page):
            plugin_stack.addWidget(self.create_plugins_page(i + 1))
        # 默认第一页
        plugin_stack.setCurrentIndex(0)

        # 添加翻页控制
        top_layout.addLayout(create_pagination_controls(plugin_stack, self._logic.plugins))

        return top_frame

    # 生成当页的插件内容，3x3的网格布局
    def create_plugins_page(self, page_num=1):
        # 功能卡片网格
        page = QWidget()
        card_grid = QGridLayout(page)
        card_grid.setSpacing(15)
        # 根据页数获取卡片对象列表
        cards = self._logic.get_page_card(page_num)
        # cards = []
        # 添加卡片
        for i in cards:
            card_grid.addWidget(i[0], i[1], i[2])
        return page
