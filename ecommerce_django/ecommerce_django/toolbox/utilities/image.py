from django.core.files.base import ContentFile
from PIL import Image
from io import BytesIO


def resize_image(image_url, destination_url=None, width=400):

    img = Image.open(image_url)
    info = img.info
    percent = (width / float(img.size[0]))
    height = int((float(img.size[1]) * float(percent)))

    img.thumbnail((width, height))
    if destination_url:
        img.save(destination_url, **info)
    else:
        img.save(image_url, **info)

    return True


def resize_image_aws(image_file, width=400, name=None):
    image_content_file = ContentFile(image_file.read())
    cropped_image = Image.open(image_content_file, 'r')
    format = cropped_image.format
    percent = (width / float(cropped_image.size[0]))
    height = int((float(cropped_image.size[1]) * float(percent)))
    cropped_image.thumbnail((width, height))
    new_image_io = BytesIO()
    cropped_image.save(new_image_io, format=format)
    return ContentFile(new_image_io.getvalue())