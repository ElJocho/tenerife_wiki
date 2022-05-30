from werkzeug.utils import secure_filename
from PIL import Image
import io
import base64

ALLOWED_IMAGE_EXTENSIONS = ('pdf', 'png', 'jpg', 'jpeg', 'PNG', 'JPG', 'JPEG', 'PDF')


def allowed_file(filename: str, allowed_extensions: tuple) -> bool:
    """Check if file has a valid ending."""
    return '.' in filename and \
           filename.rsplit('.')[-1].lower() in allowed_extensions


def cleanup_image(image):
    """Take image of any format and return it as a BytesIO file."""
    image = Image.open(image)
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, image.format)
    return base64.b64encode(img_byte_arr.getvalue()), image.format.lower()


def read_format(input):
    image = Image.open(input)
    return image.format
