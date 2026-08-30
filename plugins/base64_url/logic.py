import base64
from urllib.parse import quote, unquote


def b64_encode(text):
    return base64.b64encode(text.encode("utf-8")).decode("ascii")


def b64_decode(text):
    return base64.b64decode(text.strip(), validate=True).decode("utf-8")


def url_encode(text):
    return quote(text)


def url_decode(text):
    return unquote(text)
