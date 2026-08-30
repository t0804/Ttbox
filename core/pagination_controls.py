from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton


def create_pagination_controls(plugin_stack, plugins):
    total = len(plugins)
    per_page = 9
    max_page = (total + per_page - 1) // per_page if total > 0 else 1

    pagination_bar = QHBoxLayout()
    pagination_bar.setContentsMargins(0, 8, 0, 0)
    prev_btn = QPushButton("上一页")
    prev_btn.setObjectName("page_btn")
    page_label = QLabel(f"1/{max_page}")
    page_label.setObjectName("page_label")
    next_btn = QPushButton("下一页")
    next_btn.setObjectName("page_btn")

    def update_status():
        current = plugin_stack.currentIndex() + 1
        page_label.setText(f"{current}/{max_page}")
        prev_btn.setEnabled(current > 1)
        next_btn.setEnabled(current < max_page)

    prev_btn.clicked.connect(lambda: (
        plugin_stack.setCurrentIndex(plugin_stack.currentIndex() - 1),
        update_status()
    ) if plugin_stack.currentIndex() > 0 else None)

    next_btn.clicked.connect(lambda: (
        plugin_stack.setCurrentIndex(plugin_stack.currentIndex() + 1),
        update_status()
    ) if plugin_stack.currentIndex() + 1 < max_page else None)

    update_status()
    pagination_bar.addWidget(prev_btn)
    pagination_bar.addStretch()
    pagination_bar.addWidget(page_label)
    pagination_bar.addStretch()
    pagination_bar.addWidget(next_btn)

    return pagination_bar
