import os
from app.models import Make
from app import app
import binascii
from PIL import Image

# save image file name


def save_picture(form_picture, path):
    # generate a random hex string
    random_hex = binascii.b2a_hex(os.urandom(8))
    # split filename and extension
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = str(random_hex) + str(f_ext)
    picture_path = os.path.join(app.root_path, path, picture_fn)
    # resize image
    output_size = (300, 400)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    # return image file
    return picture_fn
