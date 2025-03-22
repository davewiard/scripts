#!/usr/bin/env python3

# loops through the command-line args and resizes the images to 1920 px along the long edge
# If the image is already smaller, the image is left as-is
# Also renames the image so it is a .jpg file

import sys
import PythonMagick
from pathlib import Path

SIZE = 1920

FILE_PATH = None
IMAGE = None

def rename(file):
    global IMAGE
    global FILE_PATH

    temp_file_path = 'new-{}.jpg'.format(FILE_PATH.stem)
    final_file_path = '{}.jpg'.format(FILE_PATH.stem)
    try:
        print('Saving file to {}'.format(temp_file_path))
        IMAGE.write(temp_file_path)
    except PythonMagick.Error as error:
        print(f"An error occurred: {error}")
    temp_file = Path(temp_file_path)
    if temp_file.is_file():
        print('Renaming {} to {}'.format(temp_file_path, final_file_path))
        FILE_PATH.unlink()
        temp_file.rename(final_file_path)


def resize(file):
    global IMAGE
    global FILE_PATH

    FILE_PATH = Path(file)
    if not FILE_PATH.is_file():
        print('File not found: ', file)
        return

    IMAGE = PythonMagick.Image(file)
    w = IMAGE.size().width()
    h = IMAGE.size().height()
    ratio = 0

    if h > w:
        if h <= SIZE:
            return

        # portrait image
        ratio = SIZE / float(h)
        new_h = SIZE
        new_w = int(w * ratio)
    else:
        if w <= SIZE:
            return
    
        # landscape image
        ratio = SIZE / float(w)
        new_w = SIZE
        new_h = int(h * ratio)

    print('Resizing image')
    IMAGE.resize('{}x{}'.format(new_w, new_h))


if __name__ == "__main__":
    files = sys.argv[1:]

    for x in files:
        resize(x)
        rename(x)
