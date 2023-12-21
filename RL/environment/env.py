#from dolphin import savestate # for loading savestates
#from dolphin import event # for resetting emulation
from os import system  # for running dolphin from command line

#TODO : Insert wrapper script here
SCRIPT_PATH = '' 
# path to dolphin config files
CONFIG_PATH = '/Dolphin/Config'
# path to ISO game file
ISO_PATH = 'Z:/MarioKartWii.rvz'
# Command line options for Dolphin
DOLPHIN_CONFIG = f'-e {ISO_PATH} -u {CONFIG_PATH} ' #--script {SCRIPT_PATH}'
# path to dolphin executable - use no GUI
DOLPHIN_PATH = '"Z:/Users/Harry Stevenson/Documents/project/hjs115/Dolphin/Build/Dolphin.exe"'

def init():
    # Open Dolphin
    system(f'{DOLPHIN_PATH} {DOLPHIN_CONFIG}')
    # Load dolphin configs
    # Open Mkwii
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