from time import sleep

import pyautogui
from ahk import AHK

ahk = AHK()


# Returns win when supplied window name. Win can be used for ahk functions involving a window
def get_window(name):
    win_title = str.encode(name)
    win = ahk.find_window(title=win_title)
    return win


# Returns absolute coords when supplied win.rect and relative coords
def get_abs_coords(win_coords, relative_coords):
    absolute_coords = (relative_coords[0] + win_coords[0], relative_coords[1] + win_coords[1])
    return absolute_coords


# Returns absolute coords when supplied a window title, relative coords or client coords, and a boolean for Client
def relative_to_absolute_coords(name, x, y, client=True):
    win = get_window(name)
    win_coords = win.rect
    if client:
        relative_coords = (x + 8, y + 31)
    else:
        relative_coords = (x, y)
    absolute_coords = get_abs_coords(win_coords, relative_coords)
    return absolute_coords


# Used for testing. Coverts mouse position to relative coords to be hard programmed into the bot
def mouse_to_relative_coords():
    window_name = input("Enter the name of the window: ")
    win = get_window(window_name)
    win_coords = win.rect
    current_coords = ahk.mouse_position
    relative_coords = (current_coords[0] - win_coords[0], current_coords[1] - win_coords[1])
    print("The relative coords are:", relative_coords)
    absolute_coords = get_abs_coords(win_coords, relative_coords)
    print("The absolute coords are:", absolute_coords)
    print("Testing relative coords in 2 seconds")
    sleep(2)
    ahk.mouse_position = absolute_coords


# Converts a list of coords to a list of absolute coords when supplied
# a window title, relative coords or client coords, and a boolean for Client
def coord_list_conversion(wizard, coord_list, client=True):
    absolute_coords = []
    for coord in coord_list:
        x = coord[0]
        y = coord[1]
        if client:
            absolute_coord = relative_to_absolute_coords(wizard, x, y)
        else:
            absolute_coord = relative_to_absolute_coords(wizard, x, y, False)
        absolute_coords.append(absolute_coord)
    return absolute_coords


# Returns relative coords when supplied client coords
def client_coords_converter(coord_list):
    output_list = []
    for coord in coord_list:
        relative_coords = (coord[0] + 8, coord[1] + 31)
        output_list.append(relative_coords)
    return output_list


def get_region():
    window_name = input("Enter the name of the window: ")
    win = get_window(window_name)
    win_coords = win.rect
    print("Collecting coords in 3 seconds")
    sleep(3)
    current_coords = ahk.mouse_position
    relative_coords_1 = (current_coords[0] - win_coords[0], current_coords[1] - win_coords[1])
    print(relative_coords_1)
    print("Collecting other coords in 5 seconds")
    sleep(5)
    current_coords = ahk.mouse_position
    relative_coords_2 = (current_coords[0] - win_coords[0], current_coords[1] - win_coords[1])
    region_coord_1 = (relative_coords_2[0] - relative_coords_1[0])
    region_coord_2 = (relative_coords_2[1] - relative_coords_1[1])
    print('region_coords = get_abs_coords(wizard, ', relative_coords_1, ', True)', sep='')
    print('region = (region_coords[0], region_coords[1], ', region_coord_1, ', ', region_coord_2, ')', sep='')


def main():
    # coord_list = [[1096, 250], [1135, 284], [966, 656]]
    # converted_coords = client_coords_converter(coord_list)
    # print(converted_coords)
    # mouse_to_relative_coords()
    # get_region()
    print("Saving first coords...")
    sleep(3)
    first_coords = pyautogui.position()
    print("Saving second coords...")
    sleep(3)
    second_coords = pyautogui.position()
    print(first_coords[0], first_coords[1], second_coords[0], second_coords[1])


if __name__ == "__main__":
    main()
