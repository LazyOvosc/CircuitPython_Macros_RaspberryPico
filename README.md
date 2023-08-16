# CircuitPython_Macros_RaspberryPico
Programmable macros on matrix keyboard using Raspberry Pico with CircuitPython

## Needed parts
- Raspberry Pico
- Some matrix keyboard(I used Genius numpad)
## Installing software
- Download [CircuitPython](https://circuitpython.org/board/raspberry_pi_pico/) and install it on your Raspberry Pico controller.
- Install [adafruit_hid library](https://circuitpython.org/libraries). Just dowload budnle and follow the instructions(needed library is in bundle)

## Needed code changes
First of all you need to determine what pins on your keyboard are row pins and what are column. In my case it was easily determined by looking at conductive traces on membrane.

Then you need to determine what code have each button. You can do that by running this code
```python
import board
import keypad

KEY_PINS = (
    board.KEY1,
    board.KEY2,
    board.KEY3,
    board.KEY4,
    board.KEY5,
    board.KEY6,
    board.KEY7,
    board.KEY8,
    board.KEY9,
    board.KEY10,
    board.KEY11,
    board.KEY12,
)

keys = keypad.Keys(KEY_PINS, value_when_pressed=False, pull=True)

while True:
    event = keys.events.get()
    if event:
        print(event)
```
Don't forget to change pins to yours.

Then change ```buttons``` list in ```info_processing``` fuction so it will fit your keyboard.

Also you can edit ```cmd_dict``` in ```item_processing``` so it will contain keys you need(for example it needs to be changed for mac). Keycodes you can find [here](https://docs.circuitpython.org/projects/hid/en/latest/_modules/adafruit_hid/keycode.html).

Then all what is left to chnage is buttons names in ```macros.txt``` file. Just change it according to your keyboard.

## How to write code in txt file

First of all I need to point that spaces between ```{key_name}```, ```-``` and ```{macros_code}``` are mandatory, and you can't have spaces between ```->``` in ```{maros_code}```.

How to code:

- Text in ```{}``` will be recognized as text and will be just printed
- Text in ```[]``` will be recognized as commands and keys inside will be pressed
- Inside ```[]``` separating keys with ```+``` would make two or more keys pressed at the same time
- ```|number``` after text in both ```{}``` and ```[]``` is time delay after executing command or printing text
- ```*number``` after ```[]``` or ```{}``` would repeat the same action several times
- ```->``` after ```[]``` or ```{}``` and followed by ```[]``` or ```{}``` would continue to do actions described after ```->```

I added all possible scenarios in my ```macros.txt``` file so you can see how it works


## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.
