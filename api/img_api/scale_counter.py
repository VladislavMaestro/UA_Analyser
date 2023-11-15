import cv2 as cv
import numpy as np
import api.constants.crop_cordinates_constants as cc


def scale_counter(path, bit_depth_one_centimeter):
    img = cv.imread(path)
    crop = img[cc.Y:cc.Y + cc.HIGH, cc.X:cc.X + cc.WITH]

    # color filter default value
    y1 = 120
    y2 = 250

    if np.sum(crop == 0) > 4000:
        y1 = 129
        y2 = 130

    hsv_model = cv.cvtColor(crop, cv.COLOR_BGR2HSV)

    h_min = np.array((0, y1, 0), np.uint8)
    h_max = np.array((255, y2, 255), np.uint8)

    # applying filter per frame in HSV model
    thresh = cv.inRange(hsv_model, h_min, h_max)

    i = 0
    j = 0
    intermediate_result = []
    index_of_result = []
    final_result = []
    pixel_search_area = 200

    while i != pixel_search_area:
        intermediate_result.append(sum(thresh[i]))
        i += 1

    while j < pixel_search_area:
        k = 0
        while j < pixel_search_area and intermediate_result[j] == 0:
            k += 1
            j += 1
            index_of_result.append(k)
        while j < pixel_search_area and intermediate_result[j] != 0:
            j += 1
            final_result.append(len(index_of_result))

    final_result = list(set(final_result))
    final_result.sort()

    n = 0
    sum_of_elements = 0
    while n != len(final_result):
        sum_of_elements += final_result[n]
        n += 1
    sum_of_elements = sum_of_elements / (2 * n)

    cv.imwrite("d:\\py\\log_img\\img_scale.jpg", thresh)
    cv.destroyAllWindows()
    return bit_depth_one_centimeter * (int(sum_of_elements))
