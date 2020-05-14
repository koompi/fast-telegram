from PIL import Image
import io


def create_thumbnail(thumb, size):
    image = Image.open(thumb)
    image.thumbnail(size)

    buf = io.BytesIO()
    image.save(buf, format='JPEG')
    byte_im = buf.getvalue()

    return byte_im
