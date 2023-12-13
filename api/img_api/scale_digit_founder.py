import cv2 as cv
import numpy as np
from collections import OrderedDict
import api.img_api.scale_counter as sc
import api.img_api.dictionary_of_numbers_patterns as dnp


def jaccard_similarity(region_of_interest, pattern_i):
    intersection = np.count_nonzero(np.logical_and(region_of_interest, pattern_i))
    union = np.count_nonzero(np.logical_or(region_of_interest, pattern_i))
    return intersection / union if union != 0 else 0.0


def pattern_matcher(image_matrix, pattern_dict, delta_x):
    digit_matches = []
    digit_position = []

    threshold_for_similarity = 0.7

    for pattern_id, pattern in pattern_dict.items():

        pattern_height, pattern_width = pattern.shape
        pattern_found = False

        for y in range(image_matrix.shape[0] - pattern_height + 1):
            for x in range(image_matrix.shape[1] - pattern_width + 1 - delta_x):

                region_of_interest = image_matrix[y:y + pattern_height, x + delta_x:x + delta_x + pattern_width]

                similarity = jaccard_similarity(region_of_interest, pattern)

                if similarity >= threshold_for_similarity:
                    if pattern_id == 7:
                        pattern_id = pattern_id + 1
                    elif pattern_id == 8:
                        pattern_id = 0
                    digit_matches.append(pattern_id)
                    digit_position.append(y)
                    pattern_found = True

            if pattern_found:
                break
                
    return digit_matches, digit_position


def number_counter(initial_image, delta_x):
    matrix = sc.img_filter(initial_image)
    pattern_dict = dnp.numbers_pattern

    numbers_matches, numbers_position = pattern_matcher(matrix, pattern_dict, delta_x - 50)

    numbers_matches = list(OrderedDict.fromkeys(numbers_matches))
    numbers_position = list(OrderedDict.fromkeys(numbers_position))

    if len(numbers_position) >= 2:
        distance_between_numbers = numbers_position[1] - numbers_position[0]
    else:
        return 0, 0

    return numbers_matches, distance_between_numbers
