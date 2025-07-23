from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys

def minify_image(image_field):
    img = Image.open(image_field)
    img = img.convert("RGB")
    buffer = BytesIO()
    img.save(buffer, format='JPEG', quality=60)
    buffer.seek(0)
    return InMemoryUploadedFile(
        buffer, 'ImageField', image_field.name, 'image/jpeg', sys.getsizeof(buffer), None
    )
