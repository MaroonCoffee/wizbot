from time import sleep

import PIL
from ahk import AHK
from sys import modules
from pynput.keyboard import Key, Controller
from multiprocessing import Process, Queue
import pyautogui
import pytesseract
import re
from PIL import ImageGrab
# import image_detection

# TODO: Just finished code to scan backpacks after a battle, haven't tested but should work just fine
# TODO: Next up is getting the main wizard to the Bazaar and teleporting all
# TODO: After that, setup bazaar end handler to get each wizard nonmaximized for the next wiz
# TODO: Finally, teleport all back and restart battle loop
# TODO: After that, everything should be done, so you can start on crash detection!

ahk = AHK()
keyboard = Controller()
wizard_name_list = ["Elijah Ash", "Elijah Bright", "Elijah Caster"]
full_wizard_name_list = ["Elijah Thunderflame", "Elijah Ash", "Elijah Bright", "Elijah Caster"]


# Returns win when supplied window name. Win can be used for ahk functions involving a window
def get_window(name):
    win_title = str.encode(name)
    win = ahk.find_window(title=win_title)
    return win


# Activates a window when supplied its name
def activate_window(name):
    win = get_window(name)
    win.activate()


# Holds down or brings up a key and then waits for a specified amount of time before continuing
def hold_key(key, down=True, special=False, delay=0.02):
    if special:
        key_press = getattr(Key, key)
        if down:
            keyboard.press(key_press)
        else:
            keyboard.release(key_press)
    else:
        if down:
            keyboard.press(key)
        else:
            keyboard.release(key)
    sleep(delay)


# Starts an auto walk for the wizard specified and then waits for a specified amount of time before continuing
def auto_walk(wizard, delay=0.1):
    activate_window(wizard)
    sleep(0.05)
    hold_key('w')
    hold_key('shift', True, True)
    hold_key('w', False)
    hold_key('shift', False, True)
    sleep(delay)


# Executes a series of clicks and then waits for a specified amount of time before continuing
def window_clicks(coord_list, delay=0.1):
    for coord in coord_list:
        ahk.click(coord[0], coord[1])
        sleep(delay)


# Returns absolute coords when supplied a window name and relative coords
def get_abs_coords(name, relative_coords, single=False):
    win = get_window(name)
    win_coords = win.rect
    if single:
        absolute_coords = (relative_coords[0] + win_coords[0], relative_coords[1] + win_coords[1])
    else:
        absolute_coords = []
        for coord in relative_coords:
            absolute_coord = (coord[0] + win_coords[0], coord[1] + win_coords[1])
            absolute_coords.append(absolute_coord)
    return absolute_coords


# Teleports wizard to main account. If wizard isn't specified, teleports all wizards.
def teleport(wizard, delay=0):
    activate_window(wizard)
    coord_list = [(777, 48), (705, 122), (454, 114), (411, 394)]
    absolute_coords = get_abs_coords(wizard, coord_list)
    window_clicks(absolute_coords)
    sleep(delay)


# Quits a wizard to the title screen
def wizard_quit(wizard, delay=0.5):
    activate_window(wizard)
    ahk.key_down('Escape')
    ahk.key_up('Escape')
    coord_list = [(263, 508), (510, 383)]
    absolute_coords = get_abs_coords(wizard, coord_list)
    window_clicks(absolute_coords)
    sleep(delay)


# Joins a wizard from the title screen
def wizard_join(wizard, delay=0.5):
    activate_window(wizard)
    coord_list = [(516, 396), (407, 599), (407, 599)]
    absolute_coords = get_abs_coords(wizard, coord_list)
    window_clicks(absolute_coords, 0.2)
    sleep(delay)


# Clears the delay shop popup after the title screen (optional)
def clear_shop(wizard, delay=0.1):
    activate_window(wizard)
    sleep(200)
    ahk.key_down('Escape')
    ahk.key_up('Escape')
    sleep(200)
    ahk.key_down('Escape')
    ahk.key_up('Escape')
    sleep(delay)


# Makes a wizard begin to spin to avoid being afk kicked
def auto_spin(wizard, delay=0.2):
    activate_window(wizard)
    hold_key("d")
    hold_key("shift", True, True)
    hold_key("d", False)
    hold_key("Shift", False, False)
    sleep(delay)


# Used to call other functions to specify which wizards should receive the command
def function_caller(func_name, name_list, delay):
    app = modules[__name__]
    for account in name_list:
        func = getattr(app, func_name)
        func(account, delay)


# Quits out a wizard and then brings them back from the title screen
def reset():
    function_caller("wizard_quit", full_wizard_name_list, 0.5)
    sleep(0.5)
    function_caller("wizard_join", full_wizard_name_list, 0.5)
    # sleep(0.5)
    # function_caller("clear_shop", full_wizard_name_list, 0.2)


# Passes the turn for a given wizard in battle
def pass_wizard(name, delay):
    activate_window(name)
    absolute_coords = get_abs_coords(name, (258, 396), True)
    ahk.click(absolute_coords)
    sleep(delay)


# Returns the coords of a specified on screen image
def get_image_coords(image, wizard, region_coords, dimensions, confidence=0.8):
    region_coords = get_abs_coords(wizard, region_coords, True)
    region = (region_coords[0], region_coords[1], dimensions[0], dimensions[1])
    image_address = 'images/' + image + '.bmp'
    image_location = pyautogui.locateOnScreen(image_address, confidence=confidence, region=region)
    if image_location is None:
        return None
    image_coords = pyautogui.center(image_location)
    return image_coords.x, image_coords.y


# Selects the correct cards in battle
def card_handler():
    activate_window("Elijah Thunderflame")
    abs_escape_coords = get_abs_coords("Elijah Thunderflame", (98, 104), True)
    ahk.mouse_move(abs_escape_coords[0], abs_escape_coords[1])
    fist_coords = get_image_coords("fist", "Elijah Thunderflame", (380, 289), (108, 79))
    abs_fist_coords = get_abs_coords("Elijah Thunderflame", fist_coords, True)
    ahk.mouse_move(abs_fist_coords[0], abs_escape_coords[1])
    ahk.click(abs_fist_coords[0], abs_fist_coords[1])
    ahk.mouse_move(abs_escape_coords[0], abs_escape_coords[1])
    meteor_coords = get_image_coords("meteor", "Elijah Thunderflame", (380, 289), (108, 79))
    abs_meteor_coords = get_abs_coords("Elijah Thunderflame", meteor_coords, True)
    ahk.mouse_move(abs_meteor_coords[0], abs_escape_coords[1])
    ahk.click(abs_meteor_coords[0], abs_meteor_coords[1])
    abs_card_coords = get_abs_coords("Elijah Thunderflame", (430, 319), True)
    ahk.double_click(abs_card_coords[0], abs_card_coords[1])


# Manages multiple processes that monitor the current battle state
def battle_end_handler():
    exit_channel = Queue()
    p1 = Process(target=battle_completed_detector, args=(exit_channel,))
    p2 = Process(target=failed_round_detector, args=(exit_channel,))
    p1.start()
    p2.start()
    while True:
        exit_code = exit_channel.get()
        if exit_code != "":
            break
    p1.terminate()
    p2.terminate()
    exit_code_handler(exit_code)


# Handles various exit codes
def exit_code_handler(exit_code):
    if exit_code == 100:
        reset()
        backpack_full = False
        for wizard in wizard_name_list:
            backpack_full = backpack_check(wizard)
            if backpack_full:
                break
        if backpack_full:
            bazaar()
        else:
            battle()


# Checks to see if the player is still in battle
def battle_completed_detector(exit_channel):
    while True:
        piggle_coords = get_image_coords("piggle", "Elijah Thunderflame", (110, 511), (54, 62))
        if piggle_coords is not None:
            break
    exit_channel.put(100)


# Checks to see if a round has failed
def failed_round_detector(exit_channel):
    while True:
        pass_coords = get_image_coords("pass", "Elijah Thunderflame", (201, 376), (100, 42))
        if pass_coords is not None:
            break
    exit_channel.put(100)


# Main battle loop function
def battle():
    activate_window("Elijah Thunderflame")
    keyboard.press('x')
    keyboard.release('x')
    sleep(14)
    function_caller("teleport", wizard_name_list, 0)
    sleep(4)
    function_caller("auto_walk", full_wizard_name_list, 0)
    sleep(6)
    card_handler()
    function_caller("pass_wizard", wizard_name_list, 0)
    activate_window("Elijah Ash")
    activate_window("Elijah Thunderflame")
    battle_end_handler()


# Main bazaar function
def bazaar():
    pass


# Sets up an account to start the selling/buying process
def initiate_bazaar(wizard):
    activate_window(wizard)
    ahk.key_down('Escape')
    ahk.key_up('Escape')
    sleep(0.2)
    coord_list = [(448, 209), (446, 248), (530, 508)]
    window_clicks(coord_list, 0.2)
    ahk.key_down('x')
    ahk.key_up('x')
    sleep(0.5)
    ahk.click(666, 174)
    item_sell(wizard)


# Sells all of a given wizard's items
def item_sell(wizard):
    category = 1
    page = 1
    while True:
        row = 1
        ahk.click(1069, 371)
        while row < 8:
            sellable = get_image_coords("sell", wizard, (566, 714), (232, 63), confidence=0.8)
            if sellable is None:
                coord_list = [(682, 749), (1150, 637), (966, 656)]
                window_clicks(coord_list)
                sleep(0.8)
            else:
                row += 1
                row_coord = 308 + (63 * row)
                ahk.click(1069, row_coord)
        category += 1
        if category == 8 and page == 1:
            category = 9
            ahk.click(1428, 299)
            page = 2
        if category == 10 and page == 2:
            category = 1
            ahk.click(1428, 299)
            page = 3
            if not section_sellable(wizard, (423, 221), (97, 89), "fire"):
                category = 2
        if category == 2 and page == 3:
            if not section_sellable(wizard, (525, 222), (103, 91), "ice", 0.9):
                category = 3
        if category == 3 and page == 3:
            category = 7
        if category == 7 and page == 3:
            if not section_sellable(wizard, (1063, 219), (107, 94), "balance"):
                category = 8
        if category == 8 and page == 3:
            if not section_sellable(wizard, (1174, 222), (104, 92), "astral"):
                category = 9
        if category == 9 and page == 3:
            break
        category_coord = 360 + (108 * category)
        ahk.click(category_coord, 268)
    empower_buy(wizard)


# Checks to see if a given section is sellable (not gray)
def section_sellable(wizard, coords, dimensions, image, confidence=0.8):
    ahk.click(890, 615)
    image_gray = get_image_coords(image, wizard, coords, dimensions, confidence)
    if image_gray is None:
        return True
    else:
        return False


# Refreshes the Bazaar waiting for empowers to be sold
def empower_buy(wizard):
    stop_buying = False
    while True:
        ahk.click(1104, 827)
        ahk.click(1008, 272)
        sleep(0.75)
        ahk.click(1149, 657)
        sleep(0.75)
        ahk.double_click(1421, 344)
        empower = get_image_coords("empower", wizard, (840, 346), (332, 214))
        if empower is not None:
            stop_buying = buy_empower(wizard, 379)
        else:
            empower = get_image_coords("empower_red", wizard, (840, 346), (332, 214))
            if empower is not None:
                stop_buying = buy_empower(wizard, 379, False, (859, 426))
            else:
                empower = get_image_coords("empower2", wizard, (840, 394), (332, 214))
                if empower is not None:
                    stop_buying = buy_empower(wizard, 420, False, (859, 426))
                else:
                    empower = get_image_coords("empower2_red", wizard, (840, 394), (332, 214))
                    if empower is not None:
                        stop_buying = buy_empower(wizard, 420, False, (859, 426))
        if stop_buying:
            break


# Checks to see if there are more than 9 empowers, and if so, buys until there are only 9 left
def buy_empower(wizard, y, first_row=True, empower_coords=(0, 0)):
    emp_price_string = (read_text((1415, y, 1485, y+26)))
    if string_has_numbers(emp_price_string):
        emp_price = string_to_int(emp_price_string)
    else:
        return
    if emp_price < 5400:
        buyable = get_image_coords('buy', wizard, (476, 771), (237, 60))
        if buyable is not None:
            return True
        emp_count_string = (read_text((1170, y, 1230, y+21)))
        if string_has_numbers(emp_count_string):
            emp_count = string_to_int(emp_count_string)
        else:
            return
        buy_amount = emp_count - 9
        if not first_row:
            ahk.click(empower_coords)
        ahk.click(590, 849)
        ahk.double_click(792, 633)
        ahk.key_down('Backspace')
        ahk.key_up('Backspace')
        ahk.type(str(buy_amount))
        ahk.click(815, 832)
        ahk.click(1149, 657)


# Returns an integer when supplied a string that may include nonnumerical characters
def string_to_int(string):
    numeric_string = re.sub("[^0-9]", "", string)
    integer = int(numeric_string)
    return integer


# Checks to see if there are any numerical characters in a supplied string
def string_has_numbers(string):
    contains_digit = False
    for character in string:
        if character.isdigit():
            contains_digit = True
    return contains_digit


# Reads on screen text and returns it when supplied a bounding box
def read_text(bbox):
    pytesseract.pytesseract.tesseract_cmd = r'bin\Tesseract-OCR\tesseract.exe'
    screen_cap = PIL.ImageGrab.grab(bbox=bbox)
    # screen_cap.save('temp.png')
    text = pytesseract.image_to_string(screen_cap, lang='eng', config='myconfig.txt')
    return text


def backpack_check(wizard):
    backpack_full = False
    activate_window(wizard)
    ahk.key_down('b')
    ahk.key_up('b')
    for num in range(75, 81):
        converted_num = str(num)
        backpack_num = get_image_coords(converted_num, wizard, (219, 509), (361, 562), confidence=0.95)
        if backpack_num is not None:
            backpack_full = True
    ahk.key_down('Escape')
    ahk.key_up('Escape')
    if backpack_full:
        return True
    else:
        return False


def main():
    battle()


if __name__ == "__main__":
    main()
