import time
import cv2 as cv


def get_img_bytes(image):
    _, img_encoded = cv.imencode(".png", image)
    return img_encoded.tobytes()


def draw_point(image, x, y, color=(0, 255, 0)):
    cv.circle(image, (x, y), 4, color, -1)


def draw_lines(image, points, color=(0, 255, 0), thickness=1):
    for i in range(1, len(points)):
        cv.line(image, points[i - 1], points[i], color=color, thickness=thickness)


def get_mouse_coordinates(window, image_key):
    image_widget = window[image_key].Widget
    x_root, y_root = image_widget.winfo_pointerx(), image_widget.winfo_pointery()
    x_image = x_root - image_widget.winfo_rootx() - 82
    y_image = y_root - image_widget.winfo_rooty() - 35
    return x_image, y_image
