#!/usr/bin/env python3

# loops through the command-line args and resizes the images to 4000 px along the long edge
# If the image is already smaller, the image is left as-is

import sys
import PythonMagick
from pathlib import Path


def resize(file):
    file_path = Path(file)
    if not file_path.is_file():
        print('File not found: ', file)
        return

    image = PythonMagick.Image(file)
    w = image.size().width()
    h = image.size().height()
    ratio = 0

    if h > w:
        if h <= 4000:
            return

        # portrait image
        ratio = 4000 / float(h)
        new_h = 4000
        new_w = int(w * ratio)
    else:
        if w <= 4000:
            return

        # landscape image
        ratio = 4000 / float(w)
        new_w = 4000
        new_h = int(h * ratio)

    image.resize('{}x{}'.format(new_w, new_h))
    image.write('new-{}'.format(file))


if __name__ == "__main__":
    files = sys.argv[1:]
    [resize(x) for x in files]
