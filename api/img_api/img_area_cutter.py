import cv2 as cv
import numpy as np


def cut_area(path, point_list):
    img_model = cv.imread(path)
    while True:
        cv.imshow("image", img_model)

        # crop the bounding rect
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

        cv.imwrite("d:\\py\\log_img\\dst.jpg", dst_model)
        status = True
        return status
    cv.destroyAllWindows()
