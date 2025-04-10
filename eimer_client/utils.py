import base64
import io

from PIL import Image


def encode_image(image_path: str) -> str:
    """
    Encode image to base64 string.
    """
    with open(image_path, "rb") as image_file:
        img = Image.open(image_file)
        img = img.resize((256, 256))
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format="PNG")
        img_byte_arr = img_byte_arr.getvalue()

    encoded_image = base64.b64encode(img_byte_arr).decode("utf-8")
    return encoded_image
