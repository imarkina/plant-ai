import io
from PIL import Image


def is_valid_image(file_image_bytes):
    try:
        Image.open(io.BytesIO(file_image_bytes)).verify()
        return True
    except (ValueError, OSError):
        return False