# Ttbox 项目知识

## 项目概述
基于 PySide6 的插件化桌面工具箱（Python）。

## 架构
```
main.py              # 入口
core/                # 核心框架
├── app.py           # 应用启动
├── plugin.py        # 插件基类 + PluginMeta 元类校验
├── plugin_manager.py# 动态插件加载
├── plugin_card.py   # 插件卡片（click 信号）
├── plugin_stack.py  # 分页容器
├── pagination_controls.py # 翻页控制
├── main_window_ui.py  # UI 层
├── main_window_logic.py # 逻辑层（UI/Logic 分离）
├── config.py        # 路径配置
├── logger.py        # 日志系统
└── style.qss        # Qt 样式表
plugins/             # 插件（动态加载）
├── calculator/      # 计算器（UI 未实现）
├── color_picker/    # 颜色拾取器
└── test_plugin/     # 测试插件
```

## 技术选型
- GUI: PySide6（从 PyQt6 迁移而来）
- 屏幕截图: mss（屏幕截图 + 像素读取）
- 虚拟环境: venv/
- IDE: PyCharm (Windows)

## 开发习惯
- dev 分支开发，中文 commit 信息 + 日期
- 使用 `.opencode/instructions.md` 记录项目知识
- 偏好 UI/逻辑分离架构
- 调试用测试代码通过注释/解注释控制，不删

## 颜色选择器插件实现要点

### 架构
```
index.py → ColorPickerPlugin.create_window()
  → color_picker_app/main_window.py → ColorPickerMainWindow
    ├─ 颜色编辑 UI（HEX/RGB/HSL 双向绑定、滑块、色块预览）
    ├─ 打开时自动最小化主 Ttbox 窗口
    └─ get_color() → screen_color_picker.start_screen_color_pick()
        └─ picker_window.py → PickerWindow（全屏取色覆盖层）
```

### 全屏取色（PickerWindow）
- **不透明窗口 + 静态截图底图**：启动时 mss 一次全屏截图作为 QPixmap 背景
- 放大镜从静态底图读取像素（17×17 像素 10 倍放大，带网格、十字准星）
- 浮动信息面板显示 HEX、RGB、POS
- 鼠标自然接收（无 grabMouse，实心窗口天然隔离底层鼠标事件）
- **左键按下存颜色 → 左键释放确认**（防止 Windows 补发释放事件到底层窗口）
- 右键/ESC/失焦取消
- `QEventLoop` 局部事件循环阻塞等待取色完成

### 窗口激活
- `QTimer.singleShot(0)` 延迟到下一轮事件循环执行
- 顺序：先 `show()` 激活自己 → 再 `minimize_main_window()`（程序还是前台时激活才有效）

### 关闭窗口时
- `closeEvent` → `restore_main_window()` 恢复主 Ttbox 窗口

## 已知遗留问题
- calculator 插件的 UI 骨架已创建但未实现具体功能
- 旧路径 `clolr_picker_app/` 仍在 git HEAD 中，工作区已替换为 `color_picker_app/`

## 常用命令
```powershell
# 运行
venv\Scripts\python main.py

# 安装依赖
pip install -r requirements.txt
```
