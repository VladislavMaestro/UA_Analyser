import os
import cv2 as cv
import numpy as np


def cut_area(img_model, point_list):
    rect = cv.boundingRect(point_list)
    x, y, w, h = rect
    cropped_img = img_model[y:y + h, x:x + w].copy()

    # make mask
    point_list = point_list - point_list.min(axis=0)
    mask = np.zeros(cropped_img.shape[:2], np.uint8)
    cv.drawContours(
        mask, [point_list], -1,
        (255, 255, 255), -1, cv.LINE_AA)

    # do bit-op
    dst_model = cv.bitwise_and(cropped_img, cropped_img, mask=mask)

    # add the white background
    background = np.ones_like(cropped_img, np.uint8) * 255
    cv.bitwise_not(background, background, mask=mask)

    img_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "log_img", "dst.jpg")

    cv.imwrite(img_path, dst_model)
    status = True
    return status
