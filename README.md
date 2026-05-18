# Ttbox

基于 PySide6 的插件化桌面工具箱。

## 快速开始

```powershell
# 创建虚拟环境（如未创建）
python -m venv venv

# 安装依赖
venv\Scripts\pip install -r requirements.txt

# 运行
venv\Scripts\python main.py
```

## 架构

```
main.py              # 入口
core/                # 核心框架
├── app.py           # 应用启动
├── plugin.py        # 插件基类 + PluginMeta 元类校验
├── plugin_manager.py# 动态插件加载
├── plugin_card.py   # 插件卡片（点击信号）
├── plugin_stack.py  # 插件分页容器
├── pagination_controls.py # 翻页控制
├── main_window_ui.py  # 主窗口 UI 层
├── main_window_logic.py # 主窗口逻辑层
├── config.py        # 路径配置
├── logger.py        # 日志系统
└── style.qss        # Qt 样式表
plugins/             # 插件目录（动态加载）
└── color_picker/    # 颜色拾取器
```

## 插件开发

在 `plugins/` 下创建子目录，结构如下：

```
plugins/your_plugin/
├── __init__.py        # 暴露 __plugin_class__
├── index.py           # 插件类定义（继承 BasePlugin）
└── ...                # 其他模块
```

`index.py` 示例：

```python
from core.plugin import BasePlugin

class YourPlugin(BasePlugin):
    @property
    def name(self):
        return '插件名称'

    @property
    def version(self) -> str:
        return '1.0.0'

    def create_window(self):
        # 打开插件窗口
        pass
```

`__init__.py` 示例：

```python
from .index import YourPlugin
__plugin_class__ = YourPlugin
```

插件需满足：
- `name` 和 `version` 必须实现为 `@property`（由 `PluginMeta` 在类定义时校验）
- `__init__.py` 中定义 `__plugin_class__` 指向插件类

## 插件：颜色选择器

支持颜色编辑（HEX/RGB/HSL 双向绑定 + 滑块调节）+ 屏幕取色。

### 使用方法

1. 点击主界面的「颜色选择器」卡片
2. 使用输入框或滑块编辑颜色
3. 点击「取色」按钮进入全屏取色模式
4. 移动鼠标预览像素放大镜和颜色信息
5. 左键确认取色 / 右键或 ESC 取消
6. 取色结果自动回绑到颜色选择器

### 取色器功能

- 全屏冻结截图作为背景
- 光标周围 17×17 像素 10 倍放大网格
- 实时显示 HEX、RGB 值及光标坐标
- 红色十字准星标记中心像素
- 点击底层不会误触（实心覆盖窗口）
