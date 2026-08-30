import hashlib


def calc_hash(text=None, file_path=None, algorithm="md5"):
    """计算哈希值。text 和 file_path 二选一。"""
    h = hashlib.new(algorithm)
    if file_path:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
    else:
        h.update(text.encode("utf-8"))
    return h.hexdigest()
