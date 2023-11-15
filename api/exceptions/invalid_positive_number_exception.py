import PySimpleGUI as sg


def check_correct_string(string):
    try:
        int(string)
        return True
    except ValueError:
        sg.popup("This string must be a positive integer")
        return False
    if string <= "0":
        sg.popup("This string must be other than 0")
        return False
