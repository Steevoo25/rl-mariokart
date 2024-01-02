# -- DOLHPIN IMPORTS --
#from dolphin import savestate # for loading savestates
#from dolphin import event # for resetting emulation
#from dolphin import gui # for status messages

# -- OTHER IMPORTS --
from pyautogui import press
from os import system  # for running dolphin from command line

#TODO : Insert wrapper script here
SCRIPT_PATH = ''
# path to dolphin config files
CONFIG_PATH = 'Z:\\project\\hjs115\\Dolphin\\Config'
# path to ISO game file
ISO_PATH = 'Z:\\ISO\\MarioKartWii.rvz'
# Command line options for Dolphin
DOLPHIN_CONFIG = f' -e {ISO_PATH} -u {CONFIG_PATH}' #--script {SCRIPT_PATH}'
# path to dolphin executable - use no GUI
DOLPHIN_PATH = 'Z:\\Users\\Harry Stevenson\\Documents\\project\\dolphin-scripting\\repo\\dolphin\\Binary\\x64\\Dolphin.exe'

    # Default savestate will be in slot 1,
    # Current issue with dolphin causing a deadlock when loading savestetes from scripts
    # https:\\github.com/TASLabz/dolphin/issues/123

def init():
# Running dolphin in command line causes some issues, so I will have to open dolphin and run the script through the gui OR use the 
    command = DOLPHIN_PATH + DOLPHIN_CONFIG
    print(command)
    # 2.)Load dolphin configs
    # 3.)Load Savestate
    # 4.) Pause Emulation
    return



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

init()