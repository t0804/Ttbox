import io
import qrcode


def generate_qr_png(text):
    """生成二维码 PNG bytes，用于显示或保存"""
    img = qrcode.make(text)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue(), img
