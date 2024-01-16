from dolphin import savestate, event, gui
from time import sleep
import os
# used for on-screen status msgs
red = 0xffff0000

# As the script is run within the dolphin executable, 
# Append the true path of scripts to import
from sys import path

venv_dir ='C:\\Users\\steve\\OneDrive\\Documents\\3rd Year\\Project\\my-project\\venv\\Lib\\site-packages'
path.append(venv_dir)

this_dir = 'C:\\Users\\steve\\OneDrive\\Documents\\3rd Year\\Project\\my-project\\RL\\dolphin_interaction_tests'
path.append(this_dir)

for pathdir in path:
    print(pathdir)
# To allow embedded python to access .dlls
dll_path_embedded = "C:\\Users\\steve\\OneDrive\\Documents\\3rd Year\\Project\\External-Repos\\Dolphin\\dolphin\\Binary\\x64\\python-embed"
os.add_dll_directory("PATH_TO_DLL")

# now import required package
import pynput as pyp

# Loads the savestate in the first slot by pressing the default hotkey (F1)
def load_using_fkey(needs_reset: bool):
    
    if needs_reset:
        # status message
        message = "loading savestate using f-key"
        print(message)

        # Using pynput to press hotkey for loading savestate in first slot
        virtual_keyboard = pyp.keyboard.Controller()
        virtual_keyboard.press(pyp.keyboard.Key.f1)
        virtual_keyboard.release(pyp.keyboard.Key.f1)

        # savestate has been loaded, now next episode can begin
        needs_reset = False
    else:
        message = "reset not required"
        print(message)
        
needs_reset = True
event.on_frameadvance(load_using_fkey(needs_reset))
print("End of script")