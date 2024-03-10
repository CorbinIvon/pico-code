import time
import board
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS

# Initialize the keyboard emulation
keyboard = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(keyboard)

# Type "Hello, World!" followed by a newline
# layout.write("Hello, World!\n")
keyboard.press(Keycode.GUI, Keycode.R)  # Keycode.GUI may be the Windows or Command key
keyboard.release_all()  # Release all keys
time.sleep(0.5)  # Wait a bit for the keypresses to be recognized
layout.write("shutdown /s /t 0\n")  # Type the command to shut down the computer