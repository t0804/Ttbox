# Ttbox 项目知识（会话存档 2026-08-30）

## 项目概述
基于 PySide6 的插件化桌面工具箱（Python），Windows 平台。

## 架构
```
main.py              # 入口
core/                # 核心框架
├── app.py           # 应用启动（加载 style.qss）
├── plugin.py        # 插件基类 + PluginMeta 元类校验
├── plugin_manager.py# 动态插件加载
├── plugin_card.py   # 插件卡片（左图标右文字，hover 手型，显示版本号）
├── plugin_stack.py  # 分页容器
├── pagination_controls.py # 翻页控制
├── main_window_ui.py  # UI 层（导航 + 首页 + 搜索过滤）
├── main_window_logic.py # 逻辑层（插件加载 + 搜索过滤）
├── config.py        # 路径配置
├── logger.py        # 日志系统
└── style.qss        # Qt 样式表（现代浅色主题，~120行）
plugins/             # 插件（动态加载）
├── calculator/      # 计算器（已有 logic.py 分离）
├── color_picker/    # 颜色拾取器 ✅ 已完成
├── timestamp_converter/ # 时间戳转换 ✅ 已完成（logic.py 已分离）
├── text_diff/       # 文本对比 ✅ 已完成（LCS diff，实时高亮）
├── json_formatter/  # JSON 格式化/校验 ✅ 已完成（logic.py 已分离）
├── hash_calc/       # 哈希计算 ✅ 已完成（logic.py 已分离）
├── base64_url/      # Base64/URL 编解码 ✅ 已完成（logic.py 已分离）
├── regex_tester/    # 正则测试器 ✅ 已完成（logic.py 已分离）
├── qr_generator/    # 二维码生成 ✅ 已完成（logic.py 已分离）
└── test_plugin/     # 测试插件
```

## 插件目录规范
每个插件必须包含：
- `__init__.py` — 暴露 `__plugin_class__`
- `index.py` — 插件类（继承 BasePlugin，实现 name/version 属性，create_window 方法）
- `logic.py` — 纯业务逻辑，零 Qt 依赖（Web 端可直接复用）
- `main_window.py` — 纯 UI，调用 logic.py

## 插件 logic.py 分离（2026-08-30 新增）
所有插件已拆分为 logic + UI 两层，Web 端可直接 import logic：
| 插件 | logic.py 提取的函数 |
|------|-------------------|
| json_formatter | `format_json()` / `compact_json()` / `verify_json()` |
| hash_calc | `calc_hash(text, file_path, algorithm)` |
| base64_url | `b64_encode()` / `b64_decode()` / `url_encode()` / `url_decode()` |
| regex_tester | `find_matches()` / `compile_pattern()` |
| qr_generator | `generate_qr_png(text)` → PNG bytes + PIL.Image |
| timestamp_converter | `offset_to_utc_str()` / `utc_str_to_timezone()` / `WEEKDAYS` |
| text_diff | `lcs_opcodes(a, b)` — 基于 LCS 的 diff，O(n*m) |

## UI 重设计（2026-08-30）
- `style.qss` 重写为现代浅色主题（白底、蓝色主色 #2563EB、圆角 8-12px、hover 阴影）
- 导航栏精简为 logo + 文字按钮，active 蓝色高亮
- 插件卡片改为左图标右文字布局（240x110），显示版本号，hover 变手型
- 搜索框：输入关键词实时过滤插件，清空恢复全部
- QSS 作为默认样式，插件窗口不满意可自行覆盖（setStyleSheet）

## 技术选型
- GUI: PySide6（从 PyQt6 迁移而来）
- 屏幕截图: mss（截图 + 像素读取）
- 二维码: qrcode[pil]（已加入 requirements.txt）
- 虚拟环境: venv/
- IDE: PyCharm (Windows)

## 开发习惯
- 单人开发，直接提交 main，中文 commit 信息
- `AGENTS.md` 记录项目知识（opencode 自动读取）
- UI/逻辑分离架构
- 调试测试代码通过注释/解注释控制，不删

## 颜色选择器插件 — 完整实现细节
### 全屏取色（PickerWindow）核心方案
- 不透明全屏窗口 + 静态 mss 截图底图（非透明窗口 + grabMouse）
- mss `.bgra` → QImage.Format_ARGB32（小端 x86 匹配 BGRA 字节序）
- `paintEvent` 绘制：背景底图 + 鼠标周围 17×17 像素 10 倍放大 + 网格 + 十字准星 + 浮动信息面板
- 左键按下存色 → 左键释放确认（分段避免 phantom click）
- 右键 / ESC / 失焦取消
### 为什么不用 grabMouse
- `grabMouse()` + `releaseMouse()` 在 Windows 上产生 phantom click
- 不透明窗口天然隔离鼠标事件，无需 grabMouse
### 关闭按钮变灰问题
- 永远不要在 `show()` 之后调用 `setWindowFlags()` → 触发 HWND 重建，丢失 WS_CLOSEBOX

## 时间戳转换插件 — 实现要点
### 架构
- Live/Manual 状态机 + 双定时器（1s 更新时间 + 1ms 更新毫秒戳）
- `eventFilter` 监听 FocusIn 切换模式
- 双向输入同步：Unix 时间戳 ↔ ISO 格式，共用 `self._now_time` 作为真相源
### 时区处理
- 存 tzinfo 对象，不存字符串
- 下拉框用 `["Local(当前时区)"] + UTC_OFFSET_LIST`

## 文本对比插件 — 实现要点
- 用真正的 LCS diff（非 Ratcliff-Obershelp），结果符合直觉（如 a=1234123123, b=12312323 → 只删 4 和 1）
- 用 `setExtraSelections` 做实时高亮（不破坏光标、不污染原文）
- 双框各自高亮：顶部红删、底部绿增（实时可编辑 + 内联差异无法共存于单只读框）

## 其他关键知识点
- `QTimer.singleShot(0, fn)` 延迟到下一事件循环迭代，非立即执行
- QEventLoop + 嵌套事件循环是 Qt 标准模态阻塞模式
- `setWindowFlags()` after `show()` on Windows → HWND 重建，可能丢失 WS_CLOSEBOX
- 插件入口 `create_window()` 中必须用 `self.xxx = XxxWindow()` 持有窗口引用，否则 Python GC 回收导致窗口闪退
- `QStackedWidget` 没有 `clear()` 方法，需要逐个 removeWidget + deleteLater
- QTextEdit `setExtraSelections` 是实时高亮的正确方式（setCharFormat 在某些环境不生效）

## 常用命令
```powershell
venv\Scripts\python main.py
pip install -r requirements.txt
```
