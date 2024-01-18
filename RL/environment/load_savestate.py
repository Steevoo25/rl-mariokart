from dolphin import savestate, event, gui
from time import sleep
import os


# As the script is run within the dolphin executable, 
# Append the true path of scripts to import
from sys import path

# Add venv dir to path to allow external packages
venv_dir ='C:\\Users\\steve\\OneDrive\\Documents\\3rd Year\\Project\\my-project\\venv\\Lib\\site-packages'
path.append(venv_dir)
# Add this dir to path to allow imports from other scripts
this_dir = 'C:\\Users\\steve\\OneDrive\\Documents\\3rd Year\\Project\\my-project\\RL\\dolphin_interaction_tests'
path.append(this_dir)

# now import required package
from pynput import keyboard

# Loads the savestate in the first slot by pressing the default hotkey (F1)
def load_using_fkey():
        # status message
        message = "loading savestate using f-key"
        print(message)

        # Using pynput to press hotkey for loading savestate in first slot
        virtual_keyboard = keyboard.Controller()

        virtual_keyboard.press(keyboard.Key.f1)
        sleep(0.1)
        virtual_keyboard.release(keyboard.Key.f1)

        # savestate has been loaded, now next episode can begin
        
        # Unregister listener
        event.on_frameadvance(None)
        print("Unregistering frameadvance listener for loading state")