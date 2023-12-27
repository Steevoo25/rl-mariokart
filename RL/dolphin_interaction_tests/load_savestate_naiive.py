from dolphin import gui, savestate
from time import sleep
from pyautogui import press
red = 0xffff0000
def load_using_api():
    message = "loading savestate using dolphin api"
    gui.add_osd_message(message, 2000,red)
    # sleep for 1 second to avoid deadlock
    sleep(1)
    savestate.load_from_slot(1)

def load_using_fkey():
    message = " loading savestate using fkey"
    gui.add_osd_message(message, 2000,red)
    # sleep for 1 second to avoid deadlock
    sleep(1)
    press('f1')

load_using_fkey()