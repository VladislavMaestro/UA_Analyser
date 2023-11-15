import cv2 as cv
import numpy as np
import api.img_api.rgb_pixels_counter as rgb

dst_path = "d:\\py\\log_img\\dst.jpg"
thresh_path = "d:\\py\\log_img\\thresh.jpg"
dst_img = cv.imread(dst_path, 0)
contours_area_result = []
final_data_sample = []


def contours_area():
    img = cv.imread(thresh_path, cv.COLOR_BGR2HSV)
    ret, thresh = cv.threshold(img, 10, 255, 0)
    cv.imwrite("d:\\py\\log_img\\new_thresh.jpg", thresh)
    contours, hierarchy = cv.findContours(thresh, 1, 2)
    for i, cnt in enumerate(contours):
        M = cv.moments(cnt)
        if M['m00'] != 0.0:
            x1 = int(M['m10'] / M['m00'])
            y1 = int(M['m01'] / M['m00'])
        area = cv.contourArea(cnt)
        contours_area_result.append(area)
    contours_area_result.sort()


def remove_duplicate(sam_list):
    return list(set(sam_list))


def max_to_total_first():
    max_area = max(remove_duplicate(contours_area_result))
    return max_area / (cv.countNonZero(dst_img))


def min_to_total_first():
    min_area = min(remove_duplicate(contours_area_result))
    return min_area / (cv.countNonZero(dst_img))


def max_to_total_second():
    temp = remove_duplicate(contours_area_result)
    temp.sort()
    max_area = temp[-2]
    return max_area / (cv.countNonZero(dst_img))


def min_to_total_second():
    temp = remove_duplicate(contours_area_result)
    temp.sort()
    min_area = temp[1]
    return min_area / (cv.countNonZero(dst_img))


def rgb_pixels_to_total_value():
    return rgb.count_pixels(dst_path) / cv.countNonZero(dst_img)


def unification():
    contours_area()
    try:
        while True:
            contours_area_result.remove(0.0)
    except ValueError:
        pass

    final_data_sample.append(len(contours_area_result))
    if len(contours_area_result) > 2:
        final_data_sample.append(10000 * (max_to_total_first()))
        final_data_sample.append(10000 * (min_to_total_first()))
        final_data_sample.append(10000 * (max_to_total_second()))
        final_data_sample.append(10000 * (min_to_total_second()))
    if len(contours_area_result) == 2:
        final_data_sample.append(10000 * (max_to_total_first()))
        final_data_sample.append(10000 * (min_to_total_first()))
        final_data_sample.append(10000 * (max_to_total_first()))
        final_data_sample.append(10000 * (min_to_total_first()))
    if len(contours_area_result) == 1:
        for i in range(4):
            final_data_sample.append(1000 * (max_to_total_first()))
    if not contours_area_result:
        for i in range(4):
            final_data_sample.append(0.0)
    final_data_sample.append(1000 * (rgb_pixels_to_total_value()))
    return final_data_sample
