from time import sleep
from ahk import AHK
from sys import modules
from pynput.keyboard import Key, Controller
# import image_detection

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


# Returns absolute coords when supplied win.rect and relative coords
def get_abs_coords(name, relative_coords):
    win = get_window(name)
    win_coords = win.rect
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
    sleep(200)
    ahk.key_down('Escape')
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
def function_caller(func_name, name_list, delay, module="empower_collection"):
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
def pass_all(name):
    coord_list = [(258, 396)]
    activate_window(name)
    absolute_coords = get_abs_coords(name, coord_list)
    window_clicks(absolute_coords)


# Main battle loop function
def battle():
    activate_window("Elijah Thunderflame")
    keyboard.press('x')
    sleep(14)
    function_caller("teleport", wizard_name_list, 0)
    sleep(4)
    function_caller("auto_walk", full_wizard_name_list, 0)
    sleep(6.5)
    # TODO: Detect cards on screen and click them


def main():
    pass


if __name__ == "__main__":
    main()
