import PySimpleGUI as sg


def check_empty_img(img_model):
    if img_model is None:
        sg.popup("Incorrect path")
        return False
