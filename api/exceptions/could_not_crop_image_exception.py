import PySimpleGUI as sg


def check_number_of_points(point_list):
    length_of_list = len(point_list)
    if length_of_list < 3:
        sg.popup("Couldn't crop image. You must put at least 3 dots")
        return False
