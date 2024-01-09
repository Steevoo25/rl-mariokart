from dolphin import gui, savestate, event
from time import sleep

# As the script is run within the dolphin executable, 
# Append the true path of scripts to import
from sys import path
venv_dir ='Z:\\project\\hjs115\\venv\\Lib\\site-packages'
path.append(venv_dir)
path.append('Z:\\project\\hjs115\\RL\\dolphin_interaction_tests')

# now import required package
from pynput.keyboard import Controller, Key

# used for osd msgs
red = 0xffff0000

def load_using_api():
    message = "loading savestate using dolphin api"
    gui.add_osd_message(message, 2000,red)
    # sleep for 1 second to avoid deadlock
    sleep(1)
    savestate.load_from_slot(1)

# Loads the savestate in the first slot by pressing the default hotkey (F1)
def load_using_fkey(needs_reset: bool):
    
    if needs_reset:
        # status message
        message = "loading savestate using f-key"
        gui.add_osd_message(message, 2000,red)

        # Using pynput to press hotkey for loading savestate in first slot
        virtual_keyboard = Controller()
        virtual_keyboard.press(Key.f1)
        virtual_keyboard.release(Key.f1)
        # savestate has been loaded, now next episode can begin
        needs_reset = False
    else:
        message = "reset not required"
        gui.add_osd_message(message, 2000,red)


event.on_frameadvance(load_using_fkey(True))

