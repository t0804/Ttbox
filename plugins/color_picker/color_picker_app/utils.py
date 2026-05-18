# Qt HSL值（h:0-359, s:0-255, l:0-255）→ 通用HSL（h:0-359, s:0-100%, l:0-100%）
def qt_hsl_to_common(h, s, l):
    # 色相：直接用（无颜色时h=-1，转成0）
    h_common = h if h != -1 else 0
    # 饱和度：Qt(0-255) → 通用(0-100%)
    s_common = round((s / 255) * 100, 1)  # 保留1位小数，更友好
    # 亮度：Qt(0-255) → 通用(0-100%)
    l_common = round((l / 255) * 100, 1)
    return h_common, s_common, l_common

# 通用HSL（h:0-359, s:0-100%, l:0-100%）→ Qt HSL（h:0-359, s:0-255, l:0-255）
def common_hsl_to_qt(h, s, l):
    # 色相：限制0-359
    h_qt = max(0, min(359, int(h)))
    # 饱和度：通用(0-100%) → Qt(0-255)
    s_qt = max(0, min(255, int((s / 100) * 255)))
    # 亮度：通用(0-100%) → Qt(0-255)
    l_qt = max(0, min(255, int((l / 100) * 255)))
    return h_qt, s_qt, l_qt
