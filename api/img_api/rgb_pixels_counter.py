import cv2 as cv
import numpy as np


def count_pixels(path):
    img_model = cv.imread(path)
    while True:
        hsv_model = cv.cvtColor(img_model, cv.COLOR_BGR2HSV)

        # formation of the initial color of the filter
        h_min = np.array((0, 120, 0), np.uint8)
        h_max = np.array((255, 255, 255), np.uint8)

        # applying a filter to a frame in the HSV model
        thresh = cv.inRange(hsv_model, h_min, h_max)

        cv.imwrite("d:\\py\\log_img\\thresh.jpg", thresh)
        return cv.countNonZero(thresh)
    cv.destroyAllWindows()
