import datetime


WEEKDAYS = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]


def offset_to_utc_str(offset):
    """将 timedelta 类型的时区偏移转为 UTC±HH:MM 格式字符串"""
    total_seconds = offset.total_seconds()
    hours = int(total_seconds // 3600)
    minutes = int(abs(total_seconds) % 3600 // 60)
    if hours > 0:
        sign = "+"
    elif hours < 0:
        sign = "-"
        hours = abs(hours)
    else:
        sign = "±"
    return f"UTC{sign}{hours:02d}:{minutes:02d}"


def utc_str_to_timezone(utc_str):
    """将 UTC 偏移字符串转为 Python timezone 对象"""
    s = utc_str.replace("UTC", "").replace("±", "+")
    sign = -1 if s.startswith("-") else 1
    s = s[1:]
    hh, mm = s.split(":")
    delta = datetime.timedelta(hours=sign * int(hh), minutes=sign * int(mm))
    return datetime.timezone(delta)
