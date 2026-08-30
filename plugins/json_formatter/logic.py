import json


def format_json(text):
    """格式化 JSON（缩进2空格）"""
    try:
        data = json.loads(text)
        return json.dumps(data, indent=2, ensure_ascii=False), None
    except json.JSONDecodeError as e:
        return None, e


def compact_json(text):
    """压缩 JSON 为单行"""
    try:
        data = json.loads(text)
        return json.dumps(data, separators=(",", ":"), ensure_ascii=False), None
    except json.JSONDecodeError as e:
        return None, e


def verify_json(text):
    """校验 JSON，返回 (合法?, error或None)"""
    try:
        json.loads(text)
        return True, None
    except json.JSONDecodeError as e:
        return False, e
