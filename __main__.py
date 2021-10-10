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
import os
import stdiomask
from cryptography.fernet import Fernet
import private
import datetime


# Base Info ------------------------------------------------------------------------------------------------------------


user_list = []
user_dictionary = {}
name_dictionary = {}
win_pos_list = [(-8, 0), (790, 0), (-8, 410), (790, 410), (790, 410)]
win_pos_dictionary = {}
ahk = AHK()
keyboard = Controller()
wizard_name_list = []
full_wizard_name_list = []
all_wizard_name_list = []
filepath = ''
fast_empower_buy = True


# Base Functions -------------------------------------------------------------------------------------------------------


# Returns win when supplied window name. Win can be used for ahk functions involving a window
def get_window(name):
    win_title = str.encode(name)
    win = ahk.find_window(title=win_title)
    return win


# Activates a window when supplied its name
def activate_window(name):
    win = get_window(name)
    win.activate()


# Executes a series of clicks
def window_clicks(coord_list, delay=0.1):
    for coord in coord_list:
        ahk.click(coord[0], coord[1])
        sleep(delay)


# Used to call other functions to specify which wizards should receive the command
def function_caller(func_name, name_list, delay):
    app = modules[__name__]
    for account in name_list:
        func = getattr(app, func_name)
        func(account, delay)


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


# Holds down or brings up a key
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


# Presses a given key down for a given amount of time
def ahk_key_press(key, duration=0.0, delay=0.02):
    ahk.key_down(key)
    sleep(duration)
    ahk.key_up(key)
    sleep(delay)


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


class DummyError(Exception):
    def __init__(self, msg):
        super().__init__(msg)


# Common Functions -----------------------------------------------------------------------------------------------------


# Starts an auto walk for the wizard specified
def auto_walk(wizard, delay=0.1):
    activate_window(wizard)
    sleep(0.05)
    hold_key('w')
    hold_key('shift', True, True)
    hold_key('w', False)
    hold_key('shift', False, True)
    sleep(delay)


# Teleports wizard to main account or waypoint account.
def teleport(wizard, delay=0, waypoint=False):
    activate_window(wizard)
    if waypoint:
        coord_list = [(777, 48), (705, 145), (454, 114), (411, 394), (781, 360)]
    else:
        coord_list = [(777, 48), (705, 122), (454, 114), (411, 394), (781, 360)]
    absolute_coords = get_abs_coords(wizard, coord_list)
    ahk_key_press('w')
    window_clicks(absolute_coords)
    sleep(delay)


# Quits a wizard to the title screen
def wizard_quit(wizard, delay=0.5):
    activate_window(wizard)
    ahk_key_press('Escape')
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


# Clears the crown shop popup after the title screen if detected
def clear_shop(wizard, delay=0.1):
    activate_window(wizard)
    crown_shop_open = get_image_coords("crownshop", wizard, (44, 143), (92, 83))
    if crown_shop_open is not None:
        ahk_key_press('Escape', 0, 0.2)
        ahk_key_press('Escape')
        sleep(delay)


# Makes a wizard begin to spin to avoid being afk kicked
def auto_spin(wizard, delay=0.2):
    activate_window(wizard)
    hold_key('d')
    hold_key('shift', True, True)
    sleep(1)
    hold_key('d', False)
    hold_key('shift', False, True)
    sleep(delay)


# Quits out a wizard and then brings them back from the title screen
def reset():
    function_caller("wizard_quit", full_wizard_name_list, 0.5)
    sleep(0.5)
    function_caller("wizard_join", full_wizard_name_list, 0.5)
    sleep(0.5)
    function_caller("clear_shop", full_wizard_name_list, 0.2)


# Teleports a given wizard to the waypoint wizard
def teleport_waypoint(wizard, delay):
    teleport(wizard, delay, True)


# Checks to see if a given wizard is in fullscreen and unfullscreens them if they are
def unfullscreen(wizard, delay):
    win = get_window(wizard)
    if (win.rect[2]) == 1920:
        ahk_key_press('Escape', 0, 0.6)
        ahk.click(1317, 397)
        ahk.click(1317, 327)
        ahk.click(1174, 852)
    sleep(delay)


# Checks the UI of a given wizard to make sure they are in the right area. If not, full_restarts program after 30 fails
def ui_check(wizard, image, region1, region2, delay, confidence=0.8):
    activate_window(wizard)
    emergency_exit = 0
    while True:
        absolute_coords = get_abs_coords(wizard, (8, 615), True)
        ahk.mouse_position = absolute_coords
        item = get_image_coords(image, wizard, region1, region2, confidence=confidence)
        if item is None:
            emergency_exit += 1
            sleep(1)
        else:
            break
        if emergency_exit >= 30:
            full_restart(("Error: " + image + " not found for wizard " + wizard))
            raise DummyError("RestartBattle")
    sleep(delay)


# Checks the UI for the spell book
def book_check(wizard, delay):
    ui_check(wizard, "book", (699, 508), (107, 125), delay)


# Battle Functions -----------------------------------------------------------------------------------------------------


# Passes the turn for a given wizard in battle
def pass_wizard(name, delay):
    activate_window(name)
    absolute_coords = get_abs_coords(name, (258, 396), True)
    ahk.click(absolute_coords)
    sleep(delay)


# Selects the correct cards in battle
def card_handler():
    activate_window(full_wizard_name_list[0])
    abs_escape_coords = get_abs_coords(full_wizard_name_list[0], (98, 104), True)
    ahk.mouse_move(abs_escape_coords[0], abs_escape_coords[1])
    fist_coords = get_image_coords("fist", full_wizard_name_list[0], (380, 289), (108, 79))
    abs_fist_coords = get_abs_coords(full_wizard_name_list[0], fist_coords, True)
    ahk.mouse_move(abs_fist_coords[0], abs_escape_coords[1])
    ahk.click(abs_fist_coords[0], abs_fist_coords[1])
    ahk.mouse_move(abs_escape_coords[0], abs_escape_coords[1])
    meteor_coords = get_image_coords("meteor", full_wizard_name_list[0], (380, 289), (108, 79))
    abs_meteor_coords = get_abs_coords(full_wizard_name_list[0], meteor_coords, True)
    ahk.mouse_move(abs_meteor_coords[0], abs_escape_coords[1])
    ahk.click(abs_meteor_coords[0], abs_meteor_coords[1])
    abs_card_coords = get_abs_coords(full_wizard_name_list[0], (430, 319), True)
    ahk.double_click(abs_card_coords[0], abs_card_coords[1])


# Manages multiple processes that monitor the current battle state
def battle_end_handler():
    exit_channel = Queue()
    p1 = Process(target=battle_completed_detector, args=(exit_channel, full_wizard_name_list))
    p2 = Process(target=failed_round_detector, args=(exit_channel, full_wizard_name_list))
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
        ahk_key_press('w', 2)
        teleport(full_wizard_name_list[0], 0, True)
        sleep(2)
        book_check(full_wizard_name_list[0], 0)
        battle_enter()
    if exit_code == 101:
        reset()
        battle_enter()


# Checks to see if the player is still in battle
def battle_completed_detector(exit_channel, full_list):
    while True:
        piggle_coords = get_image_coords("piggle", full_list[0], (110, 511), (54, 62))
        if piggle_coords is not None:
            break
    exit_channel.put(100)


# Checks to see if a round has failed
def failed_round_detector(exit_channel, full_list):
    while True:
        pass_coords = get_image_coords("pass", full_list[0], (201, 376), (100, 42))
        if pass_coords is not None:
            break
    exit_channel.put(101)


# Main battle loop function
def battle(in_dungeon=False):
    if not in_dungeon:
        activate_window(full_wizard_name_list[0])
        keyboard.press('x')
        keyboard.release('x')
        sleep(13)
        book_check(full_wizard_name_list[0], 0)
    function_caller("teleport", wizard_name_list, 0)
    function_caller("book_check", full_wizard_name_list, 0)
    function_caller("auto_walk", full_wizard_name_list, 0)
    ui_check(full_wizard_name_list[0], "meteor", (380, 289), (108, 79), 0)
    card_handler()
    function_caller("pass_wizard", wizard_name_list, 0)
    activate_window(full_wizard_name_list[1])
    activate_window(full_wizard_name_list[0])
    battle_end_handler()


# Checks all 3 of the minion accounts for full backpacks, and if not, starts battle
def battle_enter():
    activate_window(full_wizard_name_list[0])
    keyboard.press('x')
    keyboard.release('x')
    sleep(1)
    for wizard in wizard_name_list:
        check = backpack_check(wizard)
        if check:
            bazaar()
    book_check(full_wizard_name_list[0], 0)
    raise DummyError("RestartBattleInDungeon")


# Checks a given wizard's backpack to see if their backpack is full
def backpack_check(wizard):
    backpack_full = False
    activate_window(wizard)
    ahk_key_press('b')
    for num in range(75, 81):
        converted_num = str(num)
        backpack_num = get_image_coords(converted_num, wizard, (219, 509), (361, 562), confidence=0.99)
        if backpack_num is not None:
            backpack_full = True
    ahk_key_press('Escape')
    if backpack_full:
        return True
    else:
        return False


# Bazaar Functions -----------------------------------------------------------------------------------------------------


# Main bazaar function
def bazaar():
    activate_window(full_wizard_name_list[0])
    ahk_key_press('w')
    ui_check(full_wizard_name_list[0], "book", (699, 508), (107, 125), 0)
    home_coords = get_abs_coords(full_wizard_name_list[0], (649, 582), True)
    ahk.click(home_coords)
    sleep(7)
    ahk_key_press('d', 0.4, 0.2)
    ahk_key_press('w', 1.5)
    ahk_key_press('x', 0, 5)
    ahk_key_press('w', 0.6)
    function_caller("teleport", wizard_name_list, 0)
    function_caller("book_check", full_wizard_name_list, 0)
    function_caller("auto_spin", full_wizard_name_list, 0)
    function_caller("initiate_bazaar", full_wizard_name_list, 1)
    function_caller("extra_sell", full_wizard_name_list, 0.5)
    function_caller("jewel_sell", full_wizard_name_list, 0.5)
    function_caller("teleport_waypoint", full_wizard_name_list, 0)
    function_caller("book_check", full_wizard_name_list, 0)
    raise DummyError("RestartBattle")


# Sets up an account to start the selling/buying process
def initiate_bazaar(wizard, delay):
    activate_window(wizard)
    ahk_key_press('Escape', 0, 0.2)
    coord_list = [(448, 209), (446, 248), (530, 508)]
    absolute_coords = get_abs_coords(wizard, coord_list)
    window_clicks(absolute_coords)
    ahk_key_press('x')
    sleep(0.5)
    ahk.click(666, 174)
    ui_check(wizard, "bazaar_backpack", (421, 855), (83, 90), 0, confidence=0.95)
    item_sell(wizard)
    ahk.click(1456, 897)
    sleep(0.5)
    ahk_key_press('Escape', 0, 0.6)
    ahk.click(1317, 397)
    ahk.click(1317, 327)
    ahk.click(1174, 852)
    sleep(0.5)
    auto_spin(wizard)
    sleep(delay)


# Sells all of a given wizard's items
def item_sell(wizard):
    bazaar_ui = get_image_coords("bazaar_backpack", wizard, (421, 855), (83, 90), confidence=0.95)
    win = get_window(wizard)
    if (bazaar_ui is None) or ((win.rect[2]) != 1920):
        unfullscreen(wizard, 0)
        bazaar()
    category = 1
    page = 1
    while True:
        sell_streak = 0
        row = 1
        ahk.double_click(1069, 371)
        while row < 8:
            sellable = get_image_coords("sell", wizard, (566, 714), (232, 63), confidence=0.8)
            if ((category == 6) or (category == 7)) and (page == 3):
                empower = get_image_coords("empower_card", wizard, (616, 435), (133, 109), confidence=0.8)
                if empower is not None:
                    sellable = 1
                    sell_streak = 0
            if sellable is None:
                ahk.double_click(682, 749)
                ahk.click(1150, 637)
                ahk.click(966, 656)
                sell_streak += 1
            else:
                row += 1
                row_coord = 308 + (63 * row)
                ahk.double_click(1069, row_coord)
                sell_streak = 0
            if sell_streak >= 30:
                ahk.click(1456, 897)
                sleep(1.5)
                ahk_key_press('x')
                sleep(0.5)
                ahk.click(666, 174)
                category, page, row, sell_streak = 1, 1, 1, 0
                ui_check(wizard, "bazaar_backpack", (421, 855), (83, 90), 0, confidence=0.95)
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
            if not section_sellable(wizard, (636, 220), (103, 91), "storm"):
                category = 4
        if category == 4 and page == 3:
            if not section_sellable(wizard, (746, 223), (103, 91), "myth"):
                category = 5
        if category == 5 and page == 3:
            if not section_sellable(wizard, (852, 223), (103, 91), "life"):
                category = 6
        if category == 8 and page == 3:
            if not section_sellable(wizard, (1174, 222), (104, 92), "astral"):
                category = 9
        if category == 9 and page == 3:
            break
        category_coord = 360 + (108 * category)
        ahk.click(category_coord, 268)
    ahk.double_click(501, 141)
    bazaar_buy(wizard)


# Checks to see if a given section is sellable (not gray)
def section_sellable(wizard, coords, dimensions, image, confidence=0.8):
    ahk.click(890, 615)
    image_gray = get_image_coords(image, wizard, coords, dimensions, confidence)
    if image_gray is None:
        return True
    else:
        return False


# Refreshes the Bazaar waiting for empowers to be sold
def bazaar_buy(wizard):
    stop_buying = False
    empower_drought = 0
    while True:
        ahk.click(501, 141)
        ahk.click(1104, 827)
        ahk.click(1008, 272)
        sleep(0.75)
        ahk.click(1149, 657)
        sleep(0.75)
        ahk.double_click(1421, 344)
        empower = get_image_coords("empower", wizard, (840, 360), (332, 65), confidence=0.95)
        if empower is not None:
            empower_drought = 0
            stop_buying = process_empower_purchase(wizard, 379)
        else:
            empower = get_image_coords("empower_red", wizard, (840, 360), (332, 65), confidence=0.95)
            if empower is not None:
                empower_drought = 0
                stop_buying = process_empower_purchase(wizard, 379)
            else:
                empower = get_image_coords("empower2", wizard, (840, 400), (332, 65), confidence=0.95)
                if empower is not None:
                    empower_drought = 0
                    stop_buying = process_empower_purchase(wizard, 420, False, (859, 426))
                else:
                    empower = get_image_coords("empower2_red", wizard, (840, 400), (332, 65), confidence=0.95)
                    if empower is not None:
                        empower_drought = 0
                        stop_buying = process_empower_purchase(wizard, 420, False, (859, 426))
                    else:
                        empower = get_image_coords("empower2", wizard, (840, 440), (332, 65), confidence=0.95)
                        if empower is not None:
                            empower_drought = 0
                            stop_buying = process_empower_purchase(wizard, 460, False, (859, 467))
                        else:
                            empower = get_image_coords("empower2_red", wizard, (840, 440), (332, 65), confidence=0.95)
                            if empower is not None:
                                empower_drought = 0
                                stop_buying = process_empower_purchase(wizard, 460, False, (859, 467))
                            else:
                                empower_drought += 1
        if stop_buying:
            break
        if empower_drought >= 20:
            ahk.click(1456, 897)
            sleep(1.5)
            ahk_key_press('x')
            sleep(0.5)
            ahk.click(1428, 299)
            sleep(0.2)
            ahk.click(1428, 299)
            sleep(0.5)
            empower_drought = 0
            ui_check(wizard, "bazaar_cards", (421, 855), (83, 90), 0, confidence=0.95)


# Either checks to see if there are more than 9 empowers, and if so, buys until there are only 9 left, or buys all
def process_empower_purchase(wizard, y, first_row=True, empower_coords=(0, 0)):
    if not first_row:
        ahk.click(empower_coords)
    buyable = get_image_coords('buy', wizard, (476, 771), (237, 60))
    if buyable is not None:
        return True
    if not fast_empower_buy:
        emp_price_string = (read_text((1415, y, 1485, y+26)))
        if string_has_numbers(emp_price_string):
            emp_price = string_to_int(emp_price_string)
        else:
            return
        if emp_price < 5400:
            emp_count_string = (read_text((1170, y, 1230, y+21)))
            if string_has_numbers(emp_count_string):
                emp_count = string_to_int(emp_count_string)
            else:
                return
            buy_amount = emp_count - 9
            buy_empower(buy_amount)
    else:
        buy_amount = 100
        buy_empower(buy_amount)


# Buys a given amount of empowers
def buy_empower(buy_amount):
    ahk.click(590, 849)
    ahk.double_click(792, 633)
    ahk_key_press('Backspace')
    ahk.type(str(buy_amount))
    ahk.click(815, 832)
    ahk.click(1149, 657)


# Sells all the plants in a given wizard's backpack to clear out plants not sold at bazaar
def extra_sell(wizard, delay, plants=True):
    activate_window(wizard)
    ahk_key_press('b')
    if plants:
        coord_list = [(159, 530), (679, 173), (520, 172), (416, 219), (232, 491), (394, 488)]
    else:
        coord_list = [(159, 530), (679, 173), (679, 173), (416, 219), (232, 491), (394, 488)]
    absolute_coords = get_abs_coords(wizard, coord_list)
    window_clicks(absolute_coords, 0.5)
    emergency_break = 0
    while True:
        menu = get_image_coords("quick_sell_x", wizard, (658, 509), (59, 50))
        if menu is not None:
            break
        else:
            sleep(1)
            emergency_break += 1
        if emergency_break >= 20:
            if plants:
                error_name = "plants"
            else:
                error_name = "Jewels"
            full_restart(("Error: " + error_name + " sell stuck in loop for wizard " + wizard))
            raise DummyError("RestartBattle")
    ahk_key_press('Escape')
    sleep(0.5)
    x_button = get_image_coords("x_button", wizard, (658, 506), (69, 50), confidence=0.95)
    if x_button is not None:
        ahk_key_press('Escape')
        absolute_coords = get_abs_coords(wizard, (695, 532), True)
        ahk.click(absolute_coords)
        ahk_key_press('Escape')
    sleep(delay)


# Sells all the jewels of a specified wizard
def jewel_sell(wizard, delay):
    extra_sell(wizard, delay, False)


# Launch Functions -----------------------------------------------------------------------------------------------------


# Processes a given encryption key to unlock personal info from private.py
# noinspection PyBroadException
def password_processor():
    while True:
        try:
            password = stdiomask.getpass("Please enter your password: ")
            encoded_text = bytes(private.encrypted_password, 'utf-8')
            decoded_text = decrypter(password, encoded_text)
            break
        except Exception:
            print("Invalid Password!")
    password_list = decoded_text.split(" ")
    encoded_text = bytes(private.encrypted_username, 'utf-8')
    decoded_text = decrypter(password, encoded_text)
    global user_list
    user_list = decoded_text.split(" ")
    encoded_text = bytes(private.encrypted_wizard_name, 'utf-8')
    decoded_text = decrypter(password, encoded_text)
    global all_wizard_name_list
    all_wizard_name_list = decoded_text.split(",")
    global user_dictionary
    for i in range(5):
        user_dictionary[user_list[i]] = password_list[i]
    global name_dictionary
    for i in range(5):
        name_dictionary[user_list[i]] = all_wizard_name_list[i]
    global win_pos_dictionary
    for i in range(5):
        win_pos_dictionary[all_wizard_name_list[i]] = win_pos_list[i]
    global wizard_name_list
    for i in range(1, 4):
        wizard_name_list.append(all_wizard_name_list[i])
    global full_wizard_name_list
    for i in range(4):
        full_wizard_name_list.append(all_wizard_name_list[i])
    global filepath
    filepath = private.file_path


# Decrypts the given info with the given encryption password
def decrypter(password, encoded_text):
    cipher_suite = Fernet(password)
    decoded_text = str(cipher_suite.decrypt(encoded_text))
    converted_text = decoded_text[2:-1]
    return converted_text


# noinspection PyBroadException
# Launches 5 instances of Wizard101 and names the windows according to the wizard logged into.
def game_launcher(user, delay):
    wizard = name_dictionary[user]
    os.startfile(filepath)
    while True:
        try:
            activate_window("Wizard101")
            break
        except AttributeError:
            sleep(1)
    while True:
        login_button = get_image_coords("login_gray", "Wizard101", (616, 517), (159, 76))
        if login_button is not None:
            break
        else:
            sleep(1)
    coord_list = [(205, 562), (400, 563), (698, 555), (734, 487)]
    absolute_coords = get_abs_coords("Wizard101", coord_list)
    ahk.click(absolute_coords[0])
    ahk.type(user)
    ahk.click(absolute_coords[1])
    ahk.type(user_dictionary[user])
    ahk.click(absolute_coords[2])
    ahk.click(absolute_coords[3])
    while True:
        try:
            play_button = get_image_coords("launcher_play", "Wizard101", (616, 517), (159, 76))
            if play_button is not None:
                break
            else:
                sleep(1)
        except Exception:
            sleep(1)
    ahk.click(absolute_coords[2])
    sleep(2)
    while True:
        try:
            activate_window("Wizard101")
            break
        except AttributeError:
            sleep(1)
    sleep(2)
    while True:
        window = get_window("Wizard101")
        window.set_title(wizard)
        working_window = get_window(wizard)
        if working_window is not None:
            break
    win = get_window(wizard)
    window_coords = win_pos_dictionary[wizard]
    win.move(window_coords[0], window_coords[1])
    coord_list = [(414, 322), (406, 602), (27, 58)]
    absolute_coords = get_abs_coords(wizard, coord_list)
    while True:
        play_button = get_image_coords("menu_play", wizard, (304, 566), (192, 60))
        try:
            big_play_button = get_image_coords("menu_play_big", wizard, (864, 1005), (170, 52))
        except ValueError:
            big_play_button = None
        if play_button or big_play_button is not None:
            break
        else:
            ahk.click(absolute_coords[2])
            sleep(0.5)
    unfullscreen(wizard, 0.5)
    character_selector(wizard)
    ahk.click(absolute_coords[1])
    sleep(5)
    clear_shop(wizard)
    auto_spin(wizard)
    sleep(delay)


# Checks to see if the given wizard is correctly selected, and if not, selects it
def character_selector(wizard):
    character_found = False
    character = None
    if wizard == full_wizard_name_list[0]:
        character_image = "thunder"
    elif wizard == full_wizard_name_list[1]:
        character_image = "ash"
    else:
        character_found = True
        character_image = "none"
    if not character_found:
        while character is None:
            coord_list = [(57, 334), (164, 263), (230, 215), (569, 209), (628, 263), (733, 322)]
            absolute_coords = get_abs_coords(wizard, coord_list)
            for i in range(6):
                character = get_image_coords(character_image, wizard, (248, 28), (310, 36))
                if character is not None:
                    break
                else:
                    ahk.click(absolute_coords[i])
                    sleep(0.5)


# Closes all instances of wizard101 and closes the google popup following the game's closure
def close_game():
    for wizard in all_wizard_name_list:
        try:
            win = get_window(wizard)
            win.kill()
        except AttributeError:
            pass
    while True:
        try:
            win = get_window("Wizard101")
            win.kill()
        except AttributeError:
            break
    sleep(5)
    while True:
        try:
            win = get_window("Ravenwood News | Wizard101 Free Online Game")
            win.kill()
        except AttributeError:
            try:
                win = get_window("429 Too Many Requests")
                win.kill()
            except AttributeError:
                break


# Fully restarts all instances of Wizard101
def full_restart(error, closegame=True):
    if closegame:
        ct = datetime.datetime.now()
        print("Script ran into an error and restarted at:", ct)
        print(error)
        close_game()
    function_caller("game_launcher", user_list, 0)
    function_caller("teleport_waypoint", full_wizard_name_list, 0)
    function_caller("book_check", full_wizard_name_list, 0)


# Main Functions -------------------------------------------------------------------------------------------------------


# Main function
# noinspection PyBroadException
def main():
    password_processor()
    try:
        full_restart("NA", False)
    except Exception as e:
        full_restart("Error: Exception " + str(e) + " caught and forced restart.")
    in_dungeon = False
    while True:
        try:
            battle(in_dungeon)
        except Exception as e:
            if str(e) == "RestartBattleInDungeon":
                in_dungeon = True
            elif str(e) == "RestartBattle":
                in_dungeon = False
            else:
                full_restart("Error: Exception " + str(e) + " caught and forced restart.")


# Runs main function
if __name__ == "__main__":
    main()
