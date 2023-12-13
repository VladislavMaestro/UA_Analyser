import cv2 as cv
import numpy as np


def check_open_image(file_path):
    try:
        stream = open(file_path, 'rb')
        img = cv.imdecode(np.asarray(bytearray(stream.read()), dtype=np.uint8), cv.IMREAD_UNCHANGED)
        return img
    except FileNotFoundError:
        return None
