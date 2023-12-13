def count_density(found_pixels, length_of_one_centimeter, dimension):
    if int(dimension) > 1:
        length_of_one_centimeter = length_of_one_centimeter/dimension

    square_centimeter = pow(length_of_one_centimeter, 2)
    return found_pixels/square_centimeter
