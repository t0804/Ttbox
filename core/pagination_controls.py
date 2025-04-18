# 翻页控制器
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QStackedWidget

plugins = [['obj1', 'obj2', 'obj3'], ['obj4', 'obj5', 'obj6'],['obj4', 'obj5', 'obj6'],[ 'obj7', 'obj8']]
if len(plugins) % 3 == 0:
    plugins_page = len(plugins) // 3
else:
    plugins_page = len(plugins) // 3 + 1
print(plugins_page)

def pagination_controls_ui(plugin_stack):

    pagination_bar = QHBoxLayout()

    prev_btn = QPushButton("上一页")
    prev_btn.clicked.connect(show_prev_page)

    page_label = QLabel("1/3")

    next_btn = QPushButton("下一页")
    next_btn.clicked.connect(show_next_page)

    pagination_bar.addWidget(prev_btn)
    pagination_bar.addStretch()
    pagination_bar.addWidget(page_label)
    pagination_bar.addStretch()
    pagination_bar.addWidget(next_btn)

    return pagination_bar

def show_next_page(plugin_stack):
    pass
    # if plugin_stack.currentIndex() + 1 < plugins_page:
    #     plugin_stack.setCurrentIndex(plugin_stack.currentIndex() + 1)
    #     update_pagination_status()

def show_prev_page(plugin_stack):
    pass
    # if plugin_stack.currentIndex() > 0:
    #     plugin_stack.setCurrentIndex(plugin_stack.currentIndex() - 1)
    #     update_pagination_status()

def update_pagination_status(plugin_stack):
    pass
    """更新分页状态显示"""
    current = plugin_stack.currentIndex() + 1
    total = plugin_stack.count()
    # page_label.setText(f"{current}/{total}")
    # prev_btn.setEnabled(current > 1)
    # next_btn.setEnabled(current < total)