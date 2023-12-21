#from dolphin import savestate # for loading savestates
#from dolphin import event # for resetting emulation
from os import system  # for running dolphin from command line

#TODO : Insert wrapper script here
SCRIPT_PATH = '' 
# path to dolphin config files
CONFIG_PATH = 'Z:/project/hjs115/Dolphin/Config'
# path to ISO game file
ISO_PATH = 'Z:/ISO/MarioKartWii.rvz'
# Command line options for Dolphin
DOLPHIN_CONFIG = f'-e {ISO_PATH} -u {CONFIG_PATH} ' #--script {SCRIPT_PATH}'
# path to dolphin executable - use no GUI
DOLPHIN_PATH = 'Z:/project/hjs115/Dolphin/Build/DolphinNoGUI.exe'

def init():
    # Open MKWii in Dolphin
    command = f'{DOLPHIN_PATH} {DOLPHIN_CONFIG}'
    print(command)
    system(command)
    
    # Load dolphin configs
    # Load Savestate
    # Pause Emulation
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