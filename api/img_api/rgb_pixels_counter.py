import os
import cv2 as cv
import numpy as np

thresh_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "log_img", "thresh.jpg")


def count_pixels(path):
    img_model = cv.imread(path)
    while True:
        hsv_model = cv.cvtColor(img_model, cv.COLOR_BGR2HSV)

        h_min = np.array((0, 120, 0), np.uint8)
        h_max = np.array((255, 255, 255), np.uint8)

        thresh = cv.inRange(hsv_model, h_min, h_max)

        cv.imwrite(thresh_path, thresh)
        return cv.countNonZero(thresh)
    cv.destroyAllWindows()
