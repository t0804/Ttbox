import mss
from pynput import mouse
# from PySide6.QtCore import Signal
from PySide6.QtGui import QColor


# class ScreenColorPicker():
#     color_picked = Signal


def start_screen_color_pick():
    """启动屏幕取色流程"""
    # 存储取色结果
    picked_color = None

    # --- 阶段二：监听与捕获 ---
    def on_click(x, y, button, pressed):
        """
        鼠标点击监听回调函数
        重点：这是一个嵌套函数，能访问外部函数的变量
        """
        nonlocal picked_color  # 声明要修改外部变量

        # 条件1：必须是按下动作（不是释放）
        # 条件2：必须是左键
        # 条件3：我们只关心第一次有效点击
        if pressed and button == mouse.Button.left:
            print(f"捕获到点击: ({x}, {y})")  # 调试用

            # 1. 使用mss截取屏幕
            with mss.mss() as sct:
                # 定义要截取的区域：以点击点为中心的1x1像素
                # 注意：mss的坐标系是左上角为(0,0)
                monitor = {
                    "top": y,  # 上边界 = y坐标
                    "left": x,  # 左边界 = x坐标
                    "width": 1,  # 宽度1像素
                    "height": 1  # 高度1像素
                }

                # 截图（非常快，因为是1x1像素）
                screenshot = sct.grab(monitor)
                pixel = screenshot.pixel(0, 0)
                picked_color = QColor(pixel[0],pixel[1],pixel[2])
                print(f"捕获颜色: {picked_color.name()}")  # 调试用

            # 4. 返回False以停止监听器
            # 这是pynlistener的机制：返回False表示停止监听
            return False

    # --- 关键：启动全局鼠标监听 ---
    print("开始监听鼠标点击...（点击屏幕任意位置取色）")
    # 创建监听器，传入我们的回调函数
    listener = mouse.Listener(on_click=on_click)
    listener.start()  # 启动监听线程
    # 等待监听器结束（用户点击后会停止）
    listener.join()  # 这会阻塞直到on_click返回False

    return picked_color


