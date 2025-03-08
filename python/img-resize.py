#!/usr/bin/env python3

# loops through the command-line args and resizes the images to 4000 px along the long edge
# If the image is already smaller, the image is left as-is

import sys
import PythonMagick
from pathlib import Path

SIZE = 3000


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

    image.resize('{}x{}'.format(new_w, new_h))
    image.write('new-{}'.format(file))


if __name__ == "__main__":
    files = sys.argv[1:]
    [resize(x) for x in files]
