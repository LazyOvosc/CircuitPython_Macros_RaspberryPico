import keypad
import board
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
import time


const_standard_wait_time = 0.009

kbd = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(kbd)

km = keypad.KeyMatrix(
    row_pins=(board.GP1, board.GP2, board.GP3, board.GP4, board.GP5, board.GP6),
    column_pins=(board.GP7, board.GP8, board.GP9, board.GP10, board.GP11, board.GP12),
)


def file_read():
    with open('macros.txt') as f:
        lines = f.read().splitlines()
    return lines


def info_processing():
    lines = file_read()
    buttons = [(2, "+"), (3, "9"), (4, "8"), (5, "7"), (7, "BackSpace"), (9, "6"), (10, "5"), (11, "4"), (14, "Enter"),
               (15, "3"), (16, "2"), (17, "1"), (18, "00"), (21, "."), (22, "0"), (26, "NumLock"), (27, "*"), (28, "/"),  
               (33, "-")]
    keys_dict = {}
    for item in buttons:
        for i in range(len(lines)):
            if item[1] == lines[i].split()[0][1:-1]:
                if "->" not in lines[i].split()[2]:
                    keys_dict[item[0]] = [lines[i].split()[2]]
                else:
                    keys_dict[item[0]] = lines[i].split()[2].split("->")
    return keys_dict


def item_splitting(item):
    num = 1
    if item[-1].isdigit():
        for i in range(len(item) - 1, -1, -1):
            if not item[i].isdigit():
                num = int(item[i + 1:])
                item = item[:i]
                break
    if item[0] == "[":
        item = item[1:-1].split("|")
        item[0] = item[0].split("+")
        item.insert(0, "cmd")
    elif item[0] == "{":
        item = item[1:-1].split("|")
        item.insert(0, "txt")

    item.append(num)
    return item


def item_processing(item):
    wait_time = 0

    cmd_dict = {
        "backspace": Keycode.BACKSPACE,
        "enter": Keycode.ENTER,
        "numlock": Keycode.KEYPAD_NUMLOCK,
        "alt": Keycode.ALT,
        "ctrl": Keycode.CONTROL,
        "shift": Keycode.SHIFT,
        "win": Keycode.WINDOWS, 
        "capslock": Keycode.CAPS_LOCK,
        "tab": Keycode.TAB,
        "esc": Keycode.ESCAPE,
        "del": Keycode.DELETE,
        "ins": Keycode.INSERT,
        "a": Keycode.A,
        "b": Keycode.B,
        "c": Keycode.C,
        "d": Keycode.D,
        "e": Keycode.E,
        "f": Keycode.F,
        "g": Keycode.G,
        "h": Keycode.H,
        "i": Keycode.I,
        "j": Keycode.J,
        "k": Keycode.K,
        "l": Keycode.L,
        "m": Keycode.M,
        "n": Keycode.N,
        "o": Keycode.O,
        "p": Keycode.P,
        "q": Keycode.Q,
        "r": Keycode.R,
        "s": Keycode.S,
        "t": Keycode.T,
        "u": Keycode.U,
        "v": Keycode.V,
        "w": Keycode.W,
        "x": Keycode.X,
        "y": Keycode.Y,
        "z": Keycode.Z,
        "0": Keycode.ZERO,
        "1": Keycode.ONE,
        "2": Keycode.TWO,
        "3": Keycode.THREE,
        "4": Keycode.FOUR,
        "5": Keycode.FIVE,
        "6": Keycode.SIX,
        "7": Keycode.SEVEN,
        "8": Keycode.EIGHT,
        "9": Keycode.NINE,
        "f1": Keycode.F1,
        "f2": Keycode.F2,
        "f3": Keycode.F3,
        "f4": Keycode.F4,
        "f5": Keycode.F5,
        "f6": Keycode.F6,
        "f7": Keycode.F7,
        "f8": Keycode.F8,
        "f9": Keycode.F9,
        "f10": Keycode.F10,
        "f11": Keycode.F11,
        "f12": Keycode.F12
    }   
    repetition_index = 2
    if len(item) == 4:
        wait_time = float(item[2])
        repetition_index = 3
    for i in range(item[repetition_index]):
        if item[0] == "txt":
            layout.write(item[1])
        elif item[0] == "cmd":
            for cmd in item[1]:
                kbd.press(cmd_dict[cmd.lower()])
            time.sleep(const_standard_wait_time)
            for cmd in item[1]:
                kbd.release(cmd_dict[cmd.lower()])
        if wait_time < const_standard_wait_time:
            wait_time = const_standard_wait_time
            
        time.sleep(wait_time)

    return


keys_dict = info_processing()

while True:
    event = km.events.get()
    if event:
        key_number = event.key_number
        if event.pressed:
            if keys_dict[key_number] != "":
                for item in keys_dict[key_number]:
                    item = item_splitting(item)
                    item_processing(item)
        if event.released:
            pass