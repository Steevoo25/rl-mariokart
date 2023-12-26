from dolphin import savestate # for loading savestates
# from dolphin import event # for resetting emulation
from dolphin import gui # for status messages
from pyautogui import press

from os import system  # for running dolphin from command line

#TODO : Insert wrapper script here
SCRIPT_PATH = '' 
# path to dolphin config files
CONFIG_PATH = 'Z:/project/hjs115/Dolphin/Config'
# path to ISO game file
ISO_PATH = 'Z:/ISO/MarioKartWii.rvz'
# Command line options for Dolphin
DOLPHIN_CONFIG = f'-e {ISO_PATH} -u {CONFIG_PATH}' #--script {SCRIPT_PATH}'
# path to dolphin executable - use no GUI
DOLPHIN_PATH = 'Z:/project/hjs115/Dolphin/Build/Dolphin.exe'

    # Default savestate will be in slot 1,
    # Current issue with dolphin causing a deadlock when loading savestetes from scripts
    # https://github.com/TASLabz/dolphin/issues/123
    # savestate.load_from_slot(1)
    # Instead we use the load state hotkey
    # TODO: Change config so 'load state' button is on the gamecube controller and use
    # controller.set_gc_buttons() to load the state
    


def init():

    # 1.) Open MKWii in Dolphin
    # TODO: Dolphin resolution configs
    #command = f'{DOLPHIN_PATH} {DOLPHIN_CONFIG}'
    #print(command)
    #system(command)

    # 2.)Load dolphin configs
    # 3.)Load Savestate
    gui.add_osd_message("Loading state from slot 1")
    press('f1')
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