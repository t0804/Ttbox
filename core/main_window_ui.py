from PySide6.QtCore import Qt, QSize, QTimer, QDateTime
from PySide6.QtGui import QIcon, QAction

from PySide6.QtWidgets import (
    QMainWindow, QWidget,
    QGridLayout, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton,
    QFrame, QStatusBar, QStackedWidget
)

from core.pagination_controls import create_pagination_controls
from core.main_window_logic import MainWindowLogic
from core.plugin_card import PluginCard
from core.config import BASE_DIR
from core import logger

logger = logger.get_logger(__name__)


class MainWindowUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self._logic = MainWindowLogic()
        self._nav_btns = []
        self._active_idx = 0
        self.setWindowTitle("Ttbox")
        self.resize(1000, 700)

        self.setup_menubar()
        self.setup_statusbar()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QHBoxLayout(central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.navigation_content()

        self.stacked_widget = QStackedWidget()
        self.main_layout.addWidget(self.stacked_widget, stretch=1)
        self.init_pages()

    def init_pages(self):
        self.stacked_widget.addWidget(self.create_home_page())
        self.stacked_widget.addWidget(self.create_other_page())
        self.stacked_widget.addWidget(self.create_settings_page())
        self.stacked_widget.setCurrentIndex(0)
        self._update_nav()

    def create_home_page(self):
        page = QWidget()
        content_layout = QVBoxLayout(page)
        content_layout.setContentsMargins(24, 20, 24, 20)
        content_layout.setSpacing(16)

        # 顶部标题栏
        r_top = QFrame()
        r_top.setObjectName("title_bar")
        r_top.setFixedHeight(48)
        title_bar = QHBoxLayout(r_top)
        title_bar.setContentsMargins(0, 0, 0, 0)
        title = QLabel("我的工具箱")
        title.setObjectName("title_label")
        search_box = QLineEdit()
        search_box.setObjectName("search_box")
        search_box.setPlaceholderText("搜索工具...")
        search_box.setFixedWidth(240)
        search_box.textChanged.connect(self._on_search)
        title_bar.addWidget(title)
        title_bar.addStretch()
        title_bar.addWidget(search_box)
        self._search_box = search_box

        content_layout.addWidget(r_top)
        content_layout.addWidget(self.plugins_widget())
        return page

    def navigation_content(self):
        nav_frame = QFrame()
        nav_frame.setObjectName("nav_frame")
        nav_frame.setFixedWidth(200)
        nav_layout = QVBoxLayout(nav_frame)
        nav_layout.setContentsMargins(8, 12, 8, 12)
        nav_layout.setSpacing(2)

        # App 标识
        logo_label = QLabel("Ttbox")
        logo_label.setStyleSheet(
            "font-size: 18px; font-weight: bold; color: #2563EB; padding: 8px 12px 16px 12px;")
        nav_layout.addWidget(logo_label)

        items = [("全部工具", 0), ("其他", 1), ("设置", 2)]
        for text, idx in items:
            btn = QPushButton(text)
            btn.setObjectName("nav_btn")
            btn.setFixedHeight(40)
            btn.clicked.connect(lambda checked, i=idx: self._switch_page(i))
            nav_layout.addWidget(btn)
            self._nav_btns.append(btn)

        nav_layout.addStretch()
        self.main_layout.addWidget(nav_frame)

    def _switch_page(self, idx):
        self._active_idx = idx
        self.stacked_widget.setCurrentIndex(idx)
        self._update_nav()

    def _update_nav(self):
        for i, btn in enumerate(self._nav_btns):
            btn.setProperty("active", "true" if i == self._active_idx else "false")
            btn.style().unpolish(btn)
            btn.style().polish(btn)

    def setup_menubar(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("文件")
        exit_action = QAction("退出", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        edit_menu = menubar.addMenu("编辑")
        edit_menu.addAction(QAction("剪切", self))
        edit_menu.addAction(QAction("复制", self))

        help_menu = menubar.addMenu("帮助")
        help_menu.addAction(QAction("关于", self))

    def setup_statusbar(self):
        status_bar = QStatusBar()
        self.setStatusBar(status_bar)
        status_bar.showMessage("就绪")
        self.time_label = QLabel()
        status_bar.addPermanentWidget(self.time_label)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        self.update_time()

    def update_time(self):
        current_time = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
        self.time_label.setText(current_time)

    def create_other_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(QLabel("此页是其他页"))
        return page

    def create_settings_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(QLabel("此页是设置页"))
        return page

    def plugins_widget(self):
        top_frame = QFrame()
        top_layout = QVBoxLayout(top_frame)
        top_layout.setContentsMargins(0, 0, 0, 0)
        self._plugin_stack = QStackedWidget()
        top_layout.addWidget(self._plugin_stack)

        self._rebuild_grid()
        top_layout.addLayout(create_pagination_controls(self._plugin_stack, self._logic._filtered))
        return top_frame

    def _rebuild_grid(self, plugins=None):
        """用当前（或指定）插件列表重建网格"""
        src = plugins if plugins is not None else self._logic._filtered
        # QStackedWidget 没有 clear，逐个删除
        while self._plugin_stack.count():
            w = self._plugin_stack.widget(0)
            self._plugin_stack.removeWidget(w)
            w.deleteLater()
        per_page = 9
        total = len(src)
        max_page = (total + per_page - 1) // per_page if total > 0 else 1
        for i in range(max_page):
            page = QWidget()
            card_grid = QGridLayout(page)
            card_grid.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
            card_grid.setSpacing(12)
            start = i * per_page
            end = min(start + per_page, total)
            for idx, plugin in enumerate(src[start:end]):
                card = PluginCard(plugin)
                card.card_clicked.connect(self.plugin_card_click)
                card_grid.addWidget(card, idx // 3, idx % 3)
            self._plugin_stack.addWidget(page)
        self._plugin_stack.setCurrentIndex(0)

    def _on_search(self, text):
        self._logic.search(text)
        self._rebuild_grid()

    def plugin_card_click(self, plugin):
        logger.debug(f'点击了插件卡片: {plugin.name}')
        self._logic.open_plugin_window(plugin)
