import os
import time
import cv2 as cv
import numpy as np
import tkinter as tk
from pathlib import Path
import PySimpleGUI as sg
import api.img_handler.handler as hr
import api.img_api.scale_counter as sc
import api.img_api.img_area_cutter as ct
import api.img_api.img_region_tools as it
import api.math_api.density_counter as dc
import api.img_api.rgb_pixels_counter as pc
import api.img_api.img_characteristics as ic
import api.img_api.scale_digit_founder as sdf
import api.exceptions.could_not_open_image_exception as cno
import api.exceptions.could_not_define_scale_dimension_exception as cnd


def update_progress_bar(progress_counter, i):
    time.sleep(0.3)
    window['-PROGRESS-'].update(current_count=progress_counter + i)
    window['-progress_txt-'].update(str(progress_counter + i) + "%")
    window.refresh()


sg.theme('DarkGrey8')
frame_field = [
    [sg.Input(key="-INPUT-", size=(30, 1)),
     sg.FileBrowse("Browse", key="-BROWSE-", size=(7, 1)),
     sg.Button("Open", size=(7, 1))],
    [sg.Button("Рассчитать", size=(45, 2), disabled=True, key="-CALCULATE-")],
    [sg.ProgressBar(100, orientation='h', size=(24, 16), border_width=1, key='-PROGRESS-'),
     sg.Text("0%", key="-progress_txt-")],
    [sg.Text("Площадь воспаления:", key="-AREA-")],
    [sg.Text("Интенсивность воспаления:", key="-INTENSITY-")],
    [sg.Text("", key="-ANSWER-")],
    [sg.Input(key="-CAPACITY-", size=(7, 1), visible=False),
     sg.Text("Сколько пикселей в одном сантиметре на фото?", key="-capacity_txt-", visible=False)],
    [sg.Button("Продолжить", size=(45, 2), visible=False, key="-CONTINUE-")],
]

canvas_col = [
    [sg.Image(key="-IMAGE-", enable_events=True, metadata=True, size=(800, 600), expand_x=True, expand_y=True)]
]

layout = [
    [
        sg.Frame("Поле для работы:", canvas_col, key="image",
                 vertical_alignment="top", pad=(0, 0), size=(1145, 825), title_location=sg.TITLE_LOCATION_TOP),
        sg.Frame("Выберите изображение:", frame_field, vertical_alignment="top",
                 pad=(0, 0), size=(400, 825))
    ]
]

window = sg.Window("Menu", layout, finalize=True)
window.Maximize()

img_path = None
img_model = None
cords_of_point = []
draw_points_enabled = True
progress_bar_counter = 0

while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED:
        break

    if event == "Open":
        img_model_for_cutter = None
        draw_points_enabled = True

        window["-PROGRESS-"].update_bar(current_count=0)
        window["-progress_txt-"].update("0%")
        window["-ANSWER-"].update("")
        window["-AREA-"].update("Площадь воспаления:")
        window["-INTENSITY-"].update("Интенсивность воспаления:")

        img_path = values["-INPUT-"]
        img_model = cno.check_open_image(img_path)

        if img_model is None:
            sg.popup("Изображение не найдено, введите корректный путь!",
                     title="Ошибка чтения изображения", modal=True, font=("Arial Bold", 12))
        else:
            img_model_for_cutter = img_model
            img_bytes = it.get_img_bytes(img_model)

            window["-IMAGE-"].update(data=img_bytes)
            window["-CALCULATE-"].update(disabled=True)

        image_is_open = True
        cords_of_point = []

    if event == "-IMAGE-" and draw_points_enabled and img_path is not None:
        x, y = it.get_mouse_coordinates(window, "-IMAGE-")
        img_model = cno.check_open_image(img_path)

        for point in cords_of_point:
            it.draw_point(img_model, point[0], point[1])

        it.draw_point(img_model, x, y, color=(0, 255, 0))
        cords_of_point.append((x, y))
        it.draw_lines(img_model, cords_of_point)

        img_bytes = it.get_img_bytes(img_model)
        window["-IMAGE-"].update(data=img_bytes)

        if len(cords_of_point) >= 3:
            window["-CALCULATE-"].update(disabled=False)
        else:
            window["-CALCULATE-"].update(disabled=True)

    if event == "-CALCULATE-":
        if len(cords_of_point) >= 2:
            cv.line(img_model, cords_of_point[0], cords_of_point[-1], color=(0, 255, 0), thickness=1)
        img_bytes = it.get_img_bytes(img_model)
        window["-IMAGE-"].update(data=img_bytes)

        if ct.cut_area(img_model_for_cutter, np.array(cords_of_point)) is True:
            dst_path = os.path.join(Path(__file__).parent.parent, "second_new_project_for_UA", "api", "log_img",
                                    "dst.jpg")
            time.sleep(0.3)
            update_progress_bar(progress_bar_counter, 20)
            progress_bar_counter += 20

            pixels = pc.count_pixels(dst_path)
            scale_capacity, coord_x_of_first_two_shapes, coord_y_of_first_two_shapes = sc.scale_counter(img_model)

            update_progress_bar(progress_bar_counter, 20)
            progress_bar_counter += 20

            if scale_capacity > 0:
                type_of_digits, scale_numbers_capacity = sdf.number_counter(img_model, coord_x_of_first_two_shapes[0])
                scale_step_dimension = int(type_of_digits[1]) - int(type_of_digits[0])

            update_progress_bar(progress_bar_counter, 20)
            progress_bar_counter += 20

            error_break_point = True
            tolerance = 2
            delta_capacity = abs(scale_capacity - scale_numbers_capacity)

            if scale_capacity == 0 or scale_capacity > 250 or delta_capacity >= tolerance:
                window["-ANSWER-"].update("Невозможно определить масштаб:", text_color="white")
                sg.popup("               Невозможно распознать шкалу программно,\n" +
                         "введите количество пикселей для одного сантиметра вручную!",
                         title="Ошибка распознавания шкалы", modal=True, font=("Arial Bold", 12))

                window["-CAPACITY-"].update(visible=True)
                window["-capacity_txt-"].update(visible=True)
                window["-CONTINUE-"].update(visible=True)

                while error_break_point:
                    event, values = window.read()

                    if event == sg.WINDOW_CLOSED:
                        error_break_point = False

                    if event == "-CONTINUE-":
                        try:
                            capacity_value = float(values["-CAPACITY-"])

                            if capacity_value > 0:
                                scale_capacity = capacity_value
                                scale_step_dimension = 1

                                window["-CAPACITY-"].update(visible=False)
                                window["-capacity_txt-"].update(visible=False)
                                window["-CONTINUE-"].update(visible=False)
                                error_break_point = False
                            else:
                                sg.popup("Вводите только положительные числа!",
                                         title="", modal=True, font=("Arial Bold", 12))
                        except ValueError:
                            sg.popup("Вводите только числа, строка не должна быть пустой!",
                                     title="", modal=True, font=("Arial Bold", 12))

            if scale_capacity > 0:
                update_progress_bar(progress_bar_counter, 20)
                progress_bar_counter += 20
                inflamed_area = dc.count_density(pixels, scale_capacity, scale_step_dimension)
                update_progress_bar(progress_bar_counter, 20)
                progress_bar_counter += 20

                if error_break_point is False and event != sg.WINDOW_CLOSED:
                    window["-ANSWER-"].update("<<<Результат посчитан вручную>>>", text_color="white")
                elif event != sg.WINDOW_CLOSED:
                    window["-ANSWER-"].update("<<<Результат посчитан автоматически>>>", text_color="white")

                window["-AREA-"].update(f"Площадь воспаления: {round(inflamed_area, 4)} cm^2")
                if inflamed_area > 0:
                    final_data = [ic.unification()]
                    intensity_of_inflammation = hr.img_data_viewer(final_data)
                    window["-INTENSITY-"].update(f"Интенсивность воспаления: {intensity_of_inflammation}")
                    draw_points_enabled = False
                    if event != sg.WINDOW_CLOSED:
                        window["-CALCULATE-"].update(disabled=True)
            progress_bar_counter = 0
    cv.destroyAllWindows()
window.close()
