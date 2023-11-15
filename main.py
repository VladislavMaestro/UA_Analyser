import PySimpleGUI as sg
import cv2 as cv
import numpy as np
import api.img_api.img_area_cutter as ct
import api.img_api.rgb_pixels_counter as pc
import api.img_api.scale_counter as sc
import api.math_api.density_counter as dc
import api.exceptions.could_not_read_image_exception as cnr
import api.exceptions.could_not_crop_image_exception as cnc
import api.exceptions.invalid_positive_number_exception as ipn
import api.img_handler.handler as hr
import api.img_api.img_characteristics as ic


def on_event_l_button_down(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        xy = "%d,%d" % (x, y)
        cv.circle(img_model, (x, y), 4, (255, 255, 0), thickness=-1)
        cv.putText(img_model,
                   xy, (x, y),
                   cv.FONT_HERSHEY_PLAIN,
                   1.0, (0, 0, 0),
                   thickness=1)
        cv.imshow("image", img_model)
        cords_of_point.append([x, y])


layout = [[sg.Text("Select image:")],
          [sg.FileBrowse(key="-INPUT-", size=(6, 1)), sg.Text("Path:")],
          [sg.Button("Open", size=(6, 1))],
          [sg.Text("Select the bit depth of one centimeter.")],
          [sg.Text("For example one centimeter is equal to four digits.")],
          [sg.Text("By default this value is 4.")],
          [sg.Input("4", key="-BIT_DEPTH-")],
          [sg.Text("The inflamed area is:", key="-AREA-")],
          [sg.Text("Intensity of inflammation:", key="-INTENSITY-")]]

window = sg.Window("Menu", layout, size=(355, 260))

while True:
    event, values = window.read()
    cords_of_point = []

    if event == sg.WINDOW_CLOSED:
        break

    img_model = cv.imread(values["-INPUT-"])

    if event == "Open":
        if cnr.check_empty_img(img_model) is False:
            break

        if values["-BIT_DEPTH-"] == "":
            bit_depth_of_one_centimeter = 4
        else:
            if ipn.check_correct_string(values["-BIT_DEPTH-"]) is False:
                break
            bit_depth_of_one_centimeter = int(values["-BIT_DEPTH-"])

        cv.namedWindow("image")
        cv.setMouseCallback("image", on_event_l_button_down)

    while True:
        cv.imshow("image", img_model)
        if cv.waitKey(0):
            if ct.cut_area(values["-INPUT-"], np.array(cords_of_point)) is True:
                if cnc.check_number_of_points(cords_of_point) is False:
                    break
                pixels = pc.count_pixels("d:\\py\\log_img\\dst.jpg")
                inflamed_area = 0
                inflamed_area = dc.count_density(pixels,
                                                 sc.scale_counter(values["-INPUT-"],
                                                                  bit_depth_of_one_centimeter))
                window["-AREA-"].update(f"The inflamed area is: {round(inflamed_area, 4)} cm^2")
                if inflamed_area > 0:
                    final_data = []
                    data = ic.unification()
                    final_data.append(data)
                    intensity_of_inflammation = hr.img_data_viewer(final_data)
                window["-INTENSITY-"].update(f"Intensity of inflammation: {intensity_of_inflammation}")
            break
    cv.destroyAllWindows()
window.close()
