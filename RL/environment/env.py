# -- DOLHPIN IMPORTS --
#from dolphin import savestate # for loading savestates
from dolphin import event # for resetting emulation
from press_button import myGCInputs

default_controller = {"A":False,"B":False,"Up":False,"StickX":7}

# As the script is run within the dolphin executable, 
# Append the true path of scripts to import
from sys import path

# Add venv dir to path to allow external packages
venv_dir ='C:\\Users\\steve\\OneDrive\\Documents\\3rd Year\\Project\\my-project\\venv\\Lib\\site-packages'
path.append(venv_dir)
# Add this dir to path to allow imports from other scripts
this_dir = 'C:\\Users\\steve\\OneDrive\\Documents\\3rd Year\\Project\\my-project\\RL\\dolphin_interaction_tests'
path.append(this_dir)

# -- OTHER IMPORTS --
from load_savestate import load_using_fkey as load_savestate
from press_button import press_button as set_controller
# Current issue with dolphin causing a deadlock when loading savestetes from scripts
# https:\\github.com/TASLabz/dolphin/issues/123


def init():
# Running dolphin in command line causes some issues, 
# so I will have to open dolphin and run the script through the gui,
# making sure to use the correct config
    # 3.) Load Savestate
    load_savestate()
    # 4.) Reset Controller
    set_controller(default_controller)
    # 4.) Pause Emulation
    

def step():
    # Read Frame
    # Calculate rewards
    # update q network
    # identify input with highest estimated reward
    # update controller
    # advance frame?
    return
# Assumes dolphin is already open
def reset():
    # Load Default savestate
    # Reset Controller
    # wipe framedumps folder
    return