import cv2 as cv
import numpy as np


def img_filter(img_model):
    return cv.inRange(cv.cvtColor(img_model, cv.COLOR_BGR2HSV), (0, 30, 115), (45, 135, 215))


def pattern_matcher(img_path, delta_width):
    main_pattern = np.ones((3, 9 - delta_width), dtype=np.uint8)
    pattern_height, pattern_width = main_pattern.shape

    threshold_for_region_of_interest = np.sum(main_pattern) * 0.85

    main_img_matrix = img_filter(img_path)
    main_img_matrix[main_img_matrix == 255] = 1

    coordinates_y_of_first_two_shapes = []
    coordinates_x_of_first_two_shapes = []
    amount_of_shapes = 0

    delta_y = 0
    delta_x = 0

    for y in range(main_img_matrix.shape[0] - pattern_height + 1):
        for x in range(main_img_matrix.shape[1] - pattern_width + 1):

            region_of_interest = main_img_matrix[
                                 y + delta_y:y + delta_y + pattern_height, x + delta_x:x + delta_x + pattern_width]

            mae_for_region_of_interest = np.sum(region_of_interest)

            if mae_for_region_of_interest > threshold_for_region_of_interest:
                if amount_of_shapes in {0, 1}:
                    coordinates_y_of_first_two_shapes.append(y + delta_y)
                    coordinates_x_of_first_two_shapes.append(x + delta_x)
                    amount_of_shapes += 1
                    delta_y += pattern_height

                if amount_of_shapes == 1:
                    delta_x += x

                if amount_of_shapes == 2:
                    break

    if len(coordinates_y_of_first_two_shapes) < 2:
        return 0, 0, 0

    capacity_of_centimeter = coordinates_y_of_first_two_shapes[1] - coordinates_y_of_first_two_shapes[0]

    return capacity_of_centimeter, coordinates_x_of_first_two_shapes, coordinates_y_of_first_two_shapes


def scale_counter(initial_image):
    delta_width_for_pattern = 0
    return pattern_matcher(initial_image, delta_width_for_pattern)
