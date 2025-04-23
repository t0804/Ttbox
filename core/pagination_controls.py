# 翻页控制器
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton


def create_pagination_controls(plugin_stack, plugins):
    """创建分页控制器"""
    if len(plugins) % 9 == 0:
        max_page = len(plugins) // 9
    else:
        max_page = len(plugins) // 9 + 1

    pagination_bar = QHBoxLayout()
    prev_btn = QPushButton("上一页")
    page_label = QLabel(f"1/{max_page}")
    next_btn = QPushButton("下一页")

    # 定义更新函数
    def update_status():
        current = plugin_stack.currentIndex() + 1
        page_label.setText(f"{current}/{max_page}")
        prev_btn.setEnabled(current > 1)
        next_btn.setEnabled(current < max_page)

    # 使用lambda闭包捕获参数
    prev_btn.clicked.connect(lambda: (
        plugin_stack.setCurrentIndex(plugin_stack.currentIndex() - 1),
        update_status()
    ) if plugin_stack.currentIndex() > 0 else None)

    next_btn.clicked.connect(lambda: (
        plugin_stack.setCurrentIndex(plugin_stack.currentIndex() + 1),
        update_status()
    ) if plugin_stack.currentIndex() + 1 < max_page else None)

    # 初始状态
    update_status()

    pagination_bar.addWidget(prev_btn)
    pagination_bar.addStretch()
    pagination_bar.addWidget(page_label)
    pagination_bar.addStretch()
    pagination_bar.addWidget(next_btn)

    return pagination_bar
