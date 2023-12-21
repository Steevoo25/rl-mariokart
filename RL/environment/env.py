#from dolphin import savestate # for loading savestates
from subprocess import run  # for running dolphin

#TODO : Insert wrapper script here
SCRIPT_PATH = '' 
# path to dolphin config files
CONFIG_PATH = '/Dolphin/Config'
# path to ISO game file
ISO_PATH = 'Z:/Users/Harry Stevenson/Documents/OneDrive - University of Birmingham/Documents/WIIISO/Mario Kart Wii (USA) (En,Fr,Es).rvz'
# TODO: Add ISO to repo
# Command line options for Dolphin
DOLPHIN_CONFIG = f'-u {CONFIG_PATH} --script {SCRIPT_PATH} -e {ISO_PATH}' 
# path to dolphin executable - use no GUI
DOLPHIN_PATH = 'Z:/Users/Harry Stevenson/Documents/project/hjs115/Dolphin/Build/DolphinNoGUI.exe'

def init():
    # Open Dolphin
    run([DOLPHIN_PATH, DOLPHIN_CONFIG])
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

def reset():
    # Load Default savestate
    # Reset Controller
    # wipe framedumps folder
    return
init()