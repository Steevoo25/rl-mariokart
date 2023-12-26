from dolphin import gui
from pyautogui import press

red = 0xffff0000
message = "Pressing f to load savestate in slot 1"
gui.add_osd_message(message, 2000,red)
print(message)
press('f1')