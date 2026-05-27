# Ttbox 项目知识（会话存档 2026-05-25）

## 项目概述
基于 PySide6 的插件化桌面工具箱（Python），Windows 平台。

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
├── calculator/      # 计算器（UI 骨架）
├── color_picker/    # 颜色拾取器 ✅ 已完成
│   ├── index.py                 # 插件入口
│   ├── color_picker_app/
│   │   ├── main_window.py       # 主窗口 UI + minimize/restore + get_color
│   │   ├── picker_window.py     # 全屏取色覆盖层（放大镜 + 截图底图）
│   │   ├── screen_color_picker.py # QEventLoop 封装
│   │   └── utils.py             # HSL 转换工具
│   └── pyt_base_plugin.json
├── timestamp_converter/ # 时间戳转换（开发中）
│   ├── __init__.py              # 插件注册
│   ├── index.py                 # 插件入口
│   ├── main_window.py           # 主窗口：Live/Manual 状态机 + 双定时器
│   └── timestamp_converter.svg  # 图标
└── test_plugin/     # 测试插件
```

## 技术选型
- GUI: PySide6（从 PyQt6 迁移而来）
- 屏幕截图: mss（截图 + 像素读取）
- 虚拟环境: venv/
- IDE: PyCharm (Windows)

## 开发习惯
- 单人开发，直接提交 main，中文 commit 信息
- `.opencode/instructions.md` 记录项目知识
- UI/逻辑分离架构
- 调试测试代码通过注释/解注释控制，不删

## 颜色选择器插件 — 完整实现细节

### 全屏取色（PickerWindow）核心方案
- **不透明全屏窗口 + 静态 mss 截图底图**（非透明窗口 + grabMouse）
- mss `.bgra` → QImage.Format_ARGB32（小端 x86 匹配 BGRA 字节序）
- `paintEvent` 绘制：背景底图 + 鼠标周围 17×17 像素 10 倍放大 + 网格 + 十字准星 + 浮动信息面板（HEX/RGB/POS）
- **左键按下存色 → 左键释放确认**（分段避免 phantom click）
- 右键 / ESC / 失焦取消

### 为什么不用 grabMouse
- `grabMouse()` + `releaseMouse()` 在 Windows 上产生 phantom click：`ReleaseCapture()` 生成 WM_LBUTTONUP 发送给光标下窗口
- 不透明窗口天然隔离鼠标事件，无需 grabMouse

### 窗口激活流程（解决"无法置顶"问题）
1. 构造 PickerWindow，`show()` 激活窗口（新建窗口 show = 激活）
2. **再** `minimize_main_window()`（程序还是前台进程，可以正常操作）
- Windows 规则：刚最小化窗口的进程被标记为后台，无法 `SetForegroundWindow`
- 兜底方案用 Win32 `SetWindowPos` HWND_TOPMOST → HWND_NOTOPMOST，但 show() 优先

### 关闭时
- `closeEvent` → `restore_main_window()`

### 关闭按钮变灰问题
- **永远不要在 `show()` 之后调用 `setWindowFlags()`** → 触发 HWND 重建，丢失 WS_CLOSEBOX

### 200ms 延迟
- 截图前 `time.sleep(0.2)` 避免窗口阴影/动画残留

### 边缘情况处理
- 选色后焦点没有自动离开：`picker_window.close()` 同时调用，`closeEvent` 退出 QEventLoop
- PickerWindow 置灰无焦点：`setAttribute(Qt.WA_ShowWithoutActivating)` 已移除（需要焦点）

## 时间戳转换插件 — 实现要点

### 架构
```
Live/Manual 状态机 + 双定时器
├── timer_1s (1000ms): 更新 self._now_time → refresh_display()
├── timer_1ms (1ms): 仅更新毫秒戳（time.time() * 1000）
└── tick 性能优化: 秒数没变时不刷其余字段（strftime/setText 开销约 8µs/次）
```

### LIVE/MANUAL 模式
- **LIVE**: 定时器正常工作，显示当前时间
- **MANUAL**: 用户编辑输入框时（FocusIn）暂停定时器
- 使用 `eventFilter` 监听 FocusIn，不用子类或 lambda 替换
- 还原按钮恢复 LIVE 模式

### 双向输入同步
- Unix 时间戳 ↔ ISO 格式互转，共用 `self._now_time` 作为真相源
- `editingFinished` 信号（Enter/失焦）触发验证
- 输入非法 → 红框提示，不切换模式

### 时区处理
- **不要存字符串**，存 tzinfo 对象（`self._current_timezone`）
- Windows `astimezone().tzinfo` 返回的是对象，转 str 会得到"中国标准时间"（ZoneInfo 不认识）
- 下拉框用 `["Local(当前时区)"] + UTC_OFFSET_LIST`
- Local → `datetime.now().astimezone()`，其他 → `ZoneInfo(iana_name)` 或 `datetime.timezone(timedelta)`

### NTP 校准（开发中）
- HTTP API（`timeapi.org`），可配置服务器列表 + 超时
- 底部状态栏设计：QFrame 默认 hidden，校准时 show → N 秒后 auto hide

## 其他关键知识点
- `QTimer.singleShot(0, fn)` 延迟到下一事件循环迭代，非立即执行
- QEventLoop + 嵌套事件循环是 Qt 标准模态阻塞模式
- `setWindowFlags()` after `show()` on Windows → HWND 重建，可能丢失 WS_CLOSEBOX
- 插件入口 `create_window()` 中必须用 `self.xxx = XxxWindow()` 持有窗口引用，否则 Python GC 回收导致窗口闪退（详细说明见 `core/plugin.py` 中 `create_window` 的 docstring）

## 已知遗留问题
- calculator 插件 UI 骨架已创建但未实现
- timestamp_converter NTP 校准 + 底部状态栏未完成

## 常用命令
```powershell
venv\Scripts\python main.py
pip install -r requirements.txt
```
