import cv2 as cv
import io
from PIL import Image


def draw_rectangle_on_image(img_data, start_point, end_point):
    color_of_rectangle = (0, 255, 0)
    thickness_of_line = 2
    cv.rectangle(img_data, start_point, end_point, color_of_rectangle, thickness_of_line)
    return img_data


def check_scale_dimension(img_data, start_point, end_point):
    img_with_rectangle = draw_rectangle_on_image(img_data, start_point, end_point)

    img_pil = Image.fromarray(cv.cvtColor(img_with_rectangle, cv.COLOR_BGR2RGB))
    img_byte_array = io.BytesIO()
    img_pil.save(img_byte_array, format='PNG')
    img_byte_array = img_byte_array.getvalue()

    return img_byte_array
