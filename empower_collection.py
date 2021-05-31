from time import sleep
from ahk import AHK
# import image_detection

ahk = AHK()


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
def hold_key(key, down=True, delay=0.02):
    if down:
        ahk.key_down(key)
        sleep(delay)
    else:
        ahk.key_up(key)
        sleep(delay)


# Starts an auto walk for the wizard specified and then waits for a specified amount of time before continuing
def auto_walk(wizard, delay=0.1):
    activate_window(wizard)
    sleep(0.05)
    hold_key('w')
    hold_key('Shift')
    hold_key('w', False)
    hold_key('Shift', False)
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


# Teleports wizard to main account
def teleport(wizard):
    activate_window(wizard)
    coord_list = [(777, 48), (705, 122), (454, 114), (411, 394)]
    absolute_coords = get_abs_coords(wizard, coord_list)
    window_clicks(absolute_coords)


# Teleports all wizards to main account
def teleport_all():
    teleport("Elijah Ash")
    teleport("Elijah Bright")
    teleport("Elijah Caster")


# Main battle loop function
def battle():
    ahk.key_down('x')
    sleep(14)
    teleport_all()
    sleep(7)
    auto_walk("Elijah Thunderflame")
    auto_walk("Elijah Ash")
    auto_walk("Elijah Bright")
    auto_walk("Elijah Caster")
    sleep(6.5)
    # TODO: Detect cards on screen and click them
