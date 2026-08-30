import re


def find_matches(pattern, text):
    """返回所有匹配的 (start, end, group) 列表，零 Qt 依赖"""
    rx = re.compile(pattern)
    return [(m.start(), m.end(), m.group()) for m in rx.finditer(text)]


def compile_pattern(pattern):
    """编译正则，成功返回 compiled regex，失败返回 (None, error)"""
    try:
        return re.compile(pattern), None
    except re.error as e:
        return None, e
