from time import sleep
from ahk import AHK
import image_detection

ahk = AHK()


def activate_window(name):
    win_title = str.encode(name)
    win = ahk.find_window(title=win_title)
    win.activate()


def hold_key(key, down=True, delay=0.02):
    if down:
        ahk.key_down(key)
        sleep(delay)
    else:
        ahk.key_up(key)
        sleep(delay)


def auto_walk(wizard, delay=0.1):
    activate_window(wizard)
    sleep(0.05)
    hold_key('w')
    hold_key('Shift')
    hold_key('w', False)
    hold_key('Shift', False)
    sleep(delay)


def window_clicks(coord_list, delay=0.1):
    for coord in coord_list:
        ahk.click(coord[0], coord[1])
        sleep(delay)


def teleport(wizard):
    activate_window(wizard)
    coords = [[769, 17], [697, 91], [446, 83], [403, 363]]
    window_clicks(coords)


def teleport_all():
    teleport("Elijah Ash")
    teleport("Elijah Bright")
    teleport("Elijah Caster")


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
